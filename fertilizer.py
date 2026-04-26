def get_recommendation(disease):
    recommendations = {
        "blight": "Apply nitrogen-rich fertilizer and use fungicides regularly.",
        "common_rust": "Use potassium fertilizer and rust-resistant treatment.",
        "gray_leaf_spot": "Apply balanced NPK fertilizer and ensure proper irrigation.",
        "healthy": "Crop is healthy. Maintain regular fertilization practices."
    }

    return recommendations.get(disease, "No recommendation available.")