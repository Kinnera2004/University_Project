def chatbot_response(user_input, lang):
    user_input = user_input.lower()

    responses_en = {
        "blight": "Blight can be controlled using fungicides and proper fertilization.",
        "rust": "Rust disease can be reduced using resistant crops.",
        "fertilizer": "Use balanced NPK fertilizer for better growth."
    }

    responses_ml = {
        "blight": "ബ്ലൈറ്റ് രോഗം ഫംഗിസൈഡ് ഉപയോഗിച്ച് നിയന്ത്രിക്കാം.",
        "rust": "റസ്റ്റ് രോഗം പ്രതിരോധ ഇനങ്ങൾ ഉപയോഗിച്ച് കുറയ്ക്കാം.",
        "fertilizer": "NPK വളങ്ങൾ സസ്യ വളർച്ചയ്ക്ക് സഹായിക്കുന്നു."
    }

    if lang == "ml":
        for key in responses_ml:
            if key in user_input:
                return responses_ml[key]
        return "ക്ഷമിക്കണം, എനിക്ക് മനസ്സിലായില്ല."
    else:
        for key in responses_en:
            if key in user_input:
                return responses_en[key]
        return "Sorry, I didn't understand."