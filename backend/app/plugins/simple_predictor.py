#!/usr/bin/env python3
# =============================================================================
# Simple Predictor Plugin - Placeholder for ML models
# =============================================================================
# This is a simple plugin that demonstrates the architecture.
# In production, this would be replaced with actual ML models (scikit-learn, etc.)

import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.plugins.base import IntelligencePlugin

logger = logging.getLogger(__name__)


class SimplePredictor(IntelligencePlugin):
    """
    Simple predictor plugin that generates basic linear predictions.
    
    This is a placeholder that demonstrates the plugin architecture.
    In production, replace with actual ML models.
    """
    
    @property
    def name(self) -> str:
        return "simple_predictor"
    
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze data and generate predictions.
        
        Expected data format:
        {
            "entity_id": "urn:ngsi-ld:AgriSensor:sensor-123",
            "attribute": "temperature",
            "historical_data": [
                {"timestamp": "2024-01-15T10:00:00Z", "value": 20.5},
                {"timestamp": "2024-01-15T11:00:00Z", "value": 22.1},
                ...
            ],
            "prediction_horizon": 24  # hours
        }
        
        Returns:
        {
            "predictions": [
                {"timestamp": "2024-01-16T10:00:00Z", "value": 23.5},
                ...
            ],
            "confidence": 0.75,
            "model": "simple_predictor"
        }
        """
        try:
            historical_data = data.get("historical_data", [])
            if len(historical_data) < 2:
                raise ValueError("Need at least 2 historical data points")
            
            attribute = data.get("attribute", "value")
            prediction_horizon = data.get("prediction_horizon", 24)  # hours
            
            # Simple linear trend calculation
            values = [point["value"] for point in historical_data]
            recent_trend = (values[-1] - values[0]) / len(values) if len(values) > 1 else 0
            
            # Generate predictions
            predictions: List[Dict[str, Any]] = []
            last_timestamp = datetime.fromisoformat(historical_data[-1]["timestamp"].replace('Z', '+00:00'))
            last_value = values[-1]
            
            for hour in range(1, prediction_horizon + 1):
                prediction_time = last_timestamp + timedelta(hours=hour)
                # Simple linear extrapolation
                predicted_value = last_value + (recent_trend * hour)
                
                predictions.append({
                    "timestamp": prediction_time.isoformat().replace('+00:00', 'Z'),
                    "value": round(predicted_value, 2)
                })
            
            # Simple confidence calculation (degrades over time)
            confidence = max(0.5, 0.9 - (prediction_horizon / 100))
            
            return {
                "predictions": predictions,
                "confidence": round(confidence, 2),
                "model": "simple_predictor",
                "metadata": {
                    "trend": round(recent_trend, 4),
                    "data_points": len(historical_data)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in SimplePredictor.analyze: {e}", exc_info=True)
            raise

