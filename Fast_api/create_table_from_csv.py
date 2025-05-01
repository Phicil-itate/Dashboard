import pandas as pd
import sqlite3
import os
from pathlib import Path

def create_table_from_csv(csv_file_path, db_path, table_name):
    """
    Create a SQLite table with schema based on a CSV file
    
    Args:
        csv_file_path (str): Path to the CSV file
        db_path (str): Path to the SQLite database
        table_name (str): Name of the table to create
    """
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        
        # Rename Q1-Q14 columns to match our schema naming convention
        column_mapping = {
            'Q1 Can you share a memorable experience': 'Q1_MemorableExperience',
            'Q2 When choosing a digital health tool': 'Q2_ToolSelectionFactors',
            'Q3 How do you feel about the level of support': 'Q3_SupportSatisfaction',
            'Q4 In what ways, if any, do digital health tools': 'Q4_MotivationFromTech',
            'Q5 What challenges or frustrations': 'Q5_CostFrustrations',
            'Q6 Could you describe how you integrate': 'Q6_DailyIntegration',
            'Q7 Tell me about a moment when you felt': 'Q7_ConfidenceMoment',
            'Q8 What improvements or additional features': 'Q8_DesiredFeatures',
            'Q9 How do you typically handle technical difficulties': 'Q9_TechIssuesImpact',
            'Q10 In your experience, how do digital health': 'Q10_EmotionalImpact',
            'Q11 Could you share your thoughts on data privacy': 'Q11_PrivacyConcerns',
            'Q12 If you had the opportunity to advise': 'Q12_AdviceToStartups',
            'Q13 How has communication with healthcare professionals': 'Q13_ProviderCommunication',
            'Q14 Have you found any technology-based': 'Q14_PeerSupportExperience'
        }
        
        # Find matching columns using partial match
        for csv_col in df.columns:
            for prefix, target_col in column_mapping.items():
                if csv_col.startswith(prefix):
                    df = df.rename(columns={csv_col: target_col})
                    break
        
        # Data type mapping
        data_type_map = {
            'PatientID': 'TEXT',
            'Age': 'INTEGER',
            'Location': 'TEXT',
            'Gender': 'TEXT',
            'DiabetesType': 'TEXT',
            'YearsSinceDiagnosis': 'INTEGER',
            'TreatmentPlan': 'TEXT',
            'HbA1c': 'FLOAT',
            'BloodPressure': 'TEXT',
            'BMI': 'FLOAT',
            'Diet': 'TEXT',
            'Exercise': 'TEXT',
            'StressLevel': 'TEXT',
            'TechUsage': 'TEXT',
            'MainChallenges': 'TEXT',
            'Goals': 'TEXT',
            'Sentiment': 'TEXT',
            'UserQuote': 'TEXT',
            'Q1_MemorableExperience': 'TEXT',
            'Q2_ToolSelectionFactors': 'TEXT',
            'Q3_SupportSatisfaction': 'TEXT',
            'Q4_MotivationFromTech': 'TEXT',
            'Q5_CostFrustrations': 'TEXT',
            'Q6_DailyIntegration': 'TEXT',
            'Q7_ConfidenceMoment': 'TEXT',
            'Q8_DesiredFeatures': 'TEXT',
            'Q9_TechIssuesImpact': 'TEXT',
            'Q10_EmotionalImpact': 'TEXT',
            'Q11_PrivacyConcerns': 'TEXT',
            'Q12_AdviceToStartups': 'TEXT',
            'Q13_ProviderCommunication': 'TEXT',
            'Q14_PeerSupportExperience': 'TEXT',
            'Notes': 'TEXT'
        }
        
        # Generate the CREATE TABLE statement
        columns = []
        for column in df.columns:
            # Use a default of TEXT if the column isn't in our mapping
            data_type = data_type_map.get(column, 'TEXT')
            columns.append(f'"{column}" {data_type}')
        
        create_table_sql = f'CREATE TABLE IF NOT EXISTS "{table_name}"(\n  ' + ',\n  '.join(columns) + '\n);'
        
        # Create the table
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        
        # Commit and close
        conn.commit()
        conn.close()
        
        print(f"Successfully created table {table_name} with schema based on CSV")
        print(create_table_sql)
        
    except Exception as e:
        print(f"Error creating table from CSV: {e}")

def main():
    # Get the base directory of the script
    base_dir = Path(__file__).parent
    
    # Path to the CSV file
    csv_file_path = os.path.join(base_dir, 'csv', 'patient.csv')
    
    # Path to the SQLite database
    db_path = os.path.join(base_dir.parent, 'dashboard.db')
    
    # Create directory for the database if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Create the table from the CSV
    create_table_from_csv(csv_file_path, db_path, 'Patient_interview')

if __name__ == "__main__":
    main()


