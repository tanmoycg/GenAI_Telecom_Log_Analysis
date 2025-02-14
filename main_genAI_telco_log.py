from transformers import pipeline
import pandas as pd
import log_generate_parse
import os 

ANALYZED_LOG_DIR  = "analyzed_log"
ANALYZED_LOG_FILE = "analyzed_5g_detailed_logs.csv"

# Classify logs 
def classify_logs():
    # Load a classification model
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    # Define possible log categories
    categories = ["Normal Event", "Warning", "Error", "Critical Failure", "Authentication Issue"]
    # Get the logs
    logs = log_generate_parse.get_parsed_logs()
    # Classify all logs
    for log in logs:
        result = classifier(log["message"], candidate_labels=categories)
        log["classification"] = result["labels"][0]  # Take top category
        log["confidence"] = result["scores"][0]

    # Convert to DataFrame
    df_logs = pd.DataFrame(logs)

    # Save to CSV after creating the analyzed log directory 
    os.makedirs(ANALYZED_LOG_DIR, exist_ok=True)
    df_logs.to_csv(os.path.join(ANALYZED_LOG_DIR, ANALYZED_LOG_FILE), index=False)
    print(f"Log classification complete. Results saved in {ANALYZED_LOG_FILE}")

# Summarize logs
def summarize_logs():
    logs = log_generate_parse.get_raw_logs()
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    # Join logs into a single text block
    log_text = " ".join(logs[:20])
    summary = summarizer(log_text, max_length=100, min_length=30, do_sample=False)
    print("Summary of 5G Logs:")
    print(summary[0]["summary_text"])
     

if __name__ == "__main__":
    classify_logs()
    #summarize_logs()