import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Ensure project root on sys.path for src.* imports
from streamlit_app import path_setup  # noqa: F401
from src.utils.config import Config

st.header("🤖 ML Predictions & Forecasts")

# Get selected stocks from session state
selected_stocks = st.session_state.get('selected_stocks', [])

# Load predictions data
predictions_file = "data/processed/features/predictions.csv"

if os.path.exists(predictions_file):
    try:
        df = pd.read_csv(predictions_file)
        
        # Handle case where symbol column doesn't exist
        if "symbol" not in df.columns:
            st.warning("⚠️ No symbol column found in predictions data.")
            
            # Convert regression predictions to binary if needed
            if "prediction" in df.columns:
                # Check if predictions are continuous (regression) or binary
                prediction_values = df["prediction"].dropna()
                if len(prediction_values) > 0:
                    # Check if it's regression (float values between 0-1 or any range)
                    is_regression = prediction_values.dtype in ['float64', 'float32']
                    
                    if is_regression:
                        # Convert to binary: > 0.5 = UP, <= 0.5 = DOWN
                        df["prediction_binary"] = (df["prediction"] > 0.5).astype(int)
                        df["prediction_label"] = df["prediction_binary"].map({1: "UP", 0: "DOWN"})
                        df["confidence"] = abs(df["prediction"] - 0.5) * 2  # Confidence based on distance from threshold
                    else:
                        # Already binary
                        df["prediction_binary"] = df["prediction"].astype(int)
                        df["prediction_label"] = df["prediction_binary"].map({1: "UP", 0: "DOWN"})
                        df["confidence"] = 0.7  # Default confidence
                
                # Show prediction summary
                st.subheader("📈 Prediction Summary")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if "prediction_binary" in df.columns:
                        up_count = df["prediction_binary"].sum()
                        st.metric("UP Predictions", up_count)
                    else:
                        st.metric("UP Predictions", 0)
                
                with col2:
                    if "prediction_binary" in df.columns:
                        down_count = len(df) - df["prediction_binary"].sum()
                        st.metric("DOWN Predictions", down_count)
                    else:
                        st.metric("DOWN Predictions", 0)
                
                with col3:
                    if "prediction" in df.columns:
                        avg_pred = df["prediction"].mean()
                        st.metric("Avg Prediction", f"{avg_pred:.2f}")
                
                with col4:
                    if "confidence" in df.columns:
                        avg_conf = df["confidence"].mean()
                        st.metric("Avg Confidence", f"{avg_conf:.1%}")
                
                # Show prediction distribution
                if "prediction_label" in df.columns:
                    st.subheader("📊 Prediction Distribution")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        prediction_dist = df["prediction_label"].value_counts()
                        fig_pie = px.pie(
                            values=prediction_dist.values,
                            names=prediction_dist.index,
                            title="UP vs DOWN Predictions",
                            color_discrete_map={"UP": "#00ff00", "DOWN": "#ff0000"}
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    with col2:
                        # Show prediction values histogram
                        if "prediction" in df.columns:
                            fig_hist = px.histogram(
                                df,
                                x="prediction",
                                nbins=20,
                                title="Prediction Value Distribution",
                                labels={"prediction": "Prediction Score", "count": "Frequency"}
                            )
                            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Show available data
            st.subheader("📊 Available Predictions Data")
            
            # Prepare display columns
            display_cols = []
            if "prediction_label" in df.columns:
                display_cols.append("prediction_label")
            if "prediction" in df.columns:
                display_cols.append("prediction")
            if "confidence" in df.columns:
                display_cols.append("confidence")
            if "Close" in df.columns:
                display_cols.append("Close")
            if "Open" in df.columns:
                display_cols.append("Open")
            if "High" in df.columns:
                display_cols.append("High")
            if "Low" in df.columns:
                display_cols.append("Low")
            
            # Add any other columns
            other_cols = [col for col in df.columns if col not in display_cols and col not in ["prediction_binary", "target"]]
            display_cols.extend(other_cols[:5])  # Limit to 5 additional columns
            
            available_display_cols = [col for col in display_cols if col in df.columns]
            
            if available_display_cols:
                st.dataframe(df[available_display_cols].head(20), use_container_width=True, hide_index=True)
            else:
                st.dataframe(df.head(20), use_container_width=True, hide_index=True)
            
            # Regeneration button
            st.markdown("---")
            st.subheader("🔄 Regenerate Predictions")
            st.info("💡 Click the button below to regenerate predictions with symbol information and improved features.")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("🚀 Regenerate Predictions", use_container_width=True, type="primary"):
                    with st.spinner("🔄 Regenerating predictions... This may take a moment."):
                        try:
                            import subprocess
                            import sys
                            
                            # Run the prediction script
                            result = subprocess.run(
                                [sys.executable, "-m", "src.ml.predict"],
                                capture_output=True,
                                text=True,
                                timeout=120
                            )
                            
                            if result.returncode == 0:
                                st.success("✅ Predictions regenerated successfully!")
                                st.info("🔄 Refreshing page to show updated predictions...")
                                st.rerun()
                            else:
                                st.error("❌ Error regenerating predictions:")
                                st.code(result.stderr, language="text")
                                st.info("💡 Try running from terminal: `python -m src.ml.predict`")
                        except subprocess.TimeoutExpired:
                            st.error("⏱️ Prediction generation timed out. Please try again.")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                            st.info("💡 Try running from terminal: `python -m src.ml.predict`")
            
            with col2:
                st.markdown("""
                **What this does:**
                - ✅ Merges predictions with historical prices
                - ✅ Adds symbol column for multi-stock filtering
                - ✅ Adds datetime, price, and predicted_price columns
                - ✅ Converts regression predictions to UP/DOWN labels
                - ✅ Calculates confidence scores
                """)
            
            # Alternative: Manual instructions
            with st.expander("📝 Or run manually from terminal"):
                st.code("python regenerate_predictions.py", language="bash")
                st.markdown("**Or:**")
                st.code("python -m src.ml.predict", language="bash")
        elif "symbol" in df.columns:
            stocks_to_filter = selected_stocks if selected_stocks else Config.STOCKS
            df = df[df["symbol"].isin(stocks_to_filter)]
            
            # Convert datetime if needed
            if "datetime" in df.columns:
                df['datetime'] = pd.to_datetime(df['datetime'])
                df = df.sort_values('datetime')
            
            # Multi-stock prediction comparison
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("📊 Prediction Trends")
                
                # Plot predictions over time
                if "predicted_price" in df.columns and "price" in df.columns:
                    fig = go.Figure()
                    stocks_to_display = selected_stocks if selected_stocks else Config.STOCKS
                    for stock in stocks_to_display:
                        stock_df = df[df["symbol"] == stock]
                        if not stock_df.empty:
                            fig.add_trace(go.Scatter(
                                x=stock_df['datetime'],
                                y=stock_df['price'],
                                mode='lines+markers',
                                name=f'{stock} Actual',
                                line=dict(color='blue', width=2)
                            ))
                            fig.add_trace(go.Scatter(
                                x=stock_df['datetime'],
                                y=stock_df['predicted_price'],
                                mode='lines+markers',
                                name=f'{stock} Predicted',
                                line=dict(color='red', width=2, dash='dash')
                            ))
                    
                    fig.update_layout(
                        title="Actual vs Predicted Prices",
                        xaxis_title="Date",
                        yaxis_title="Price ($)",
                        height=500,
                        hovermode='x unified',
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("📈 Latest Predictions")
                
                # Show latest predictions for each stock
                stocks_to_display = selected_stocks if selected_stocks else Config.STOCKS
                for stock in stocks_to_display:
                    stock_df = df[df["symbol"] == stock]
                    if not stock_df.empty:
                        latest = stock_df.iloc[-1]
                        trend = latest.get("prediction", 0)
                        confidence = latest.get("confidence", 0)
                        predicted_price = latest.get("predicted_price", 0)
                        actual_price = latest.get("price", 0)
                        
                        # Prediction direction
                        if trend == 1 or (predicted_price > actual_price):
                            trend_text = "📈 UP"
                            trend_color = "success"
                        else:
                            trend_text = "📉 DOWN"
                            trend_color = "error"
                        
                        st.metric(
                            label=stock,
                            value=trend_text,
                            delta=f"Confidence: {confidence:.1%}" if confidence else None
                        )
                        
                        if predicted_price > 0:
                            st.caption(f"Predicted: ${predicted_price:.2f}")
                            if actual_price > 0:
                                change = predicted_price - actual_price
                                change_pct = (change / actual_price * 100) if actual_price > 0 else 0
                                st.caption(f"Change: {change:+.2f} ({change_pct:+.2f}%)")
            
            # Prediction accuracy metrics
            st.subheader("📊 Prediction Accuracy Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if "confidence" in df.columns:
                    avg_confidence = df["confidence"].mean()
                    st.metric("Average Confidence", f"{avg_confidence:.1%}")
            
            with col2:
                high_confidence = len(df[df.get("confidence", 0) > 0.7]) if "confidence" in df.columns else 0
                total = len(df)
                st.metric("High Confidence Predictions", f"{high_confidence}/{total}")
            
            with col3:
                if "prediction" in df.columns:
                    # Handle both regression (continuous) and classification (binary) predictions
                    prediction_values = df["prediction"]
                    if prediction_values.dtype in ['int64', 'int32']:
                        # Binary classification
                        up_predictions = len(df[df["prediction"] == 1])
                    else:
                        # Regression - convert to binary using threshold
                        up_predictions = len(df[df["prediction"] > 0.5])
                    st.metric("UP Predictions", up_predictions)
            
            with col4:
                if "prediction" in df.columns:
                    # Handle both regression and classification
                    prediction_values = df["prediction"]
                    if prediction_values.dtype in ['int64', 'int32']:
                        # Binary classification
                        down_predictions = len(df[df["prediction"] == 0])
                    else:
                        # Regression - convert to binary using threshold
                        down_predictions = len(df[df["prediction"] <= 0.5])
                    st.metric("DOWN Predictions", down_predictions)
            
            # Multi-stock comparison table
            st.subheader("📋 Detailed Predictions")
            
            # Show latest predictions for all selected stocks
            latest_predictions = []
            stocks_to_display = selected_stocks if selected_stocks else Config.STOCKS
            for stock in stocks_to_display:
                stock_df = df[df["symbol"] == stock]
                if not stock_df.empty:
                    latest = stock_df.iloc[-1].to_dict()
                    latest_predictions.append(latest)
            
            if latest_predictions:
                comparison_df = pd.DataFrame(latest_predictions)
                display_cols = ["symbol", "datetime", "price", "predicted_price", "prediction", "confidence"]
                available_cols = [col for col in display_cols if col in comparison_df.columns]
                st.dataframe(comparison_df[available_cols], use_container_width=True, hide_index=True)
            
            # Historical predictions table
            st.subheader("📜 Historical Predictions")
            
            # Stock selector for detailed view
            selected_stock = st.selectbox(
                "Select Stock for Detailed View",
                options=selected_stocks if selected_stocks else Config.STOCKS,
                key="ml_predictions_stock"
            )
            
            stock_df = df[df["symbol"] == selected_stock] if "symbol" in df.columns else df
            
            if not stock_df.empty:
                # Format for display
                display_df = stock_df.copy()
                if "prediction" in display_df.columns:
                    display_df["prediction"] = display_df["prediction"].map({1: "UP", 0: "DOWN"})
                if "confidence" in display_df.columns:
                    display_df["confidence"] = display_df["confidence"].apply(lambda x: f"{x:.1%}" if pd.notna(x) else "N/A")
                
                st.dataframe(display_df.tail(20), use_container_width=True, hide_index=True)
                
                # Download button
                csv = stock_df.to_csv(index=False)
                st.download_button(
                    label=f"📥 Download Predictions for {selected_stock}",
                    data=csv,
                    file_name=f"ml_predictions_{selected_stock}.csv",
                    mime="text/csv"
                )
            
            # Regenerate predictions button
            st.markdown("---")
            st.subheader("🔄 Regenerate Predictions")
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("🚀 Regenerate Predictions", use_container_width=True, type="primary", key="regenerate_with_symbol"):
                    with st.spinner("🔄 Regenerating predictions... This may take a moment."):
                        try:
                            import subprocess
                            import sys
                            
                            # Run the prediction script
                            result = subprocess.run(
                                [sys.executable, "-m", "src.ml.predict"],
                                capture_output=True,
                                text=True,
                                timeout=120
                            )
                            
                            if result.returncode == 0:
                                st.success("✅ Predictions regenerated successfully!")
                                st.info("🔄 Refreshing page to show updated predictions...")
                                st.rerun()
                            else:
                                st.error("❌ Error regenerating predictions:")
                                st.code(result.stderr, language="text")
                                st.info("💡 Try running from terminal: `python -m src.ml.predict`")
                        except subprocess.TimeoutExpired:
                            st.error("⏱️ Prediction generation timed out. Please try again.")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                            st.info("💡 Try running from terminal: `python -m src.ml.predict`")
            
            with col2:
                st.markdown("""
                **What this does:**
                - ✅ Updates predictions with latest data
                - ✅ Refreshes symbol information
                - ✅ Recalculates confidence scores
                - ✅ Updates price predictions
                """)
    except Exception as e:
        st.error(f"Error loading predictions: {e}")
        st.info("Please ensure predictions have been generated")
else:
    st.error(f"Predictions file not found: {predictions_file}")
    st.info("Please run the ML prediction script first:")
    st.code("python src/ml/predict.py")
    
    # Add button to run ML predictions
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("🤖 Generate Predictions", use_container_width=True, type="primary"):
            with st.spinner("🤖 Generating predictions... This may take a moment."):
                try:
                    import subprocess
                    import sys
                    
                    # Run the prediction script
                    result = subprocess.run(
                        [sys.executable, "-m", "src.ml.predict"],
                        capture_output=True,
                        text=True,
                        timeout=120
                    )
                    
                    if result.returncode == 0:
                        st.success("✅ Predictions generated successfully!")
                        st.info("🔄 Refreshing page to show updated predictions...")
                        st.rerun()
                    else:
                        st.error("❌ Error generating predictions:")
                        st.code(result.stderr, language="text")
                        if result.stdout:
                            st.code(result.stdout, language="text")
                        st.info("💡 Try running from terminal: `python -m src.ml.predict`")
                except subprocess.TimeoutExpired:
                    st.error("⏱️ Prediction generation timed out. Please try again.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    st.info("💡 Try running from terminal: `python -m src.ml.predict`")
    
    with col2:
        st.markdown("""
        **What this does:**
        - ✅ Generates ML predictions for stock prices
        - ✅ Creates UP/DOWN predictions with confidence scores
        - ✅ Updates predictions.csv file
        - ✅ Uses trained ML model for forecasting
        """)