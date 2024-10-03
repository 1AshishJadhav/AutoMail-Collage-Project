import pandas as pd

# Assuming your Excel file is named 'student_attendance.xlsx' and the sheet is 'Sheet1'
file_path =  "E:\\Projects\\Voice Reach\\testdata.xlsx"
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Clean column names by removing leading/trailing spaces
df.columns = df.columns.str.strip()

# Function to classify students based on their attendance
def classify_attendance(attendance):
    if attendance > 0.75:
        return '100% > 75%'
    elif 0.50 < attendance <= 0.75:
        return '75% > 50%'
    elif attendance <= 0.50:
        return '50% > 25%'
    else:
        return 'Invalid'

# Apply the classification function to create a new column
df['Attendance Category'] = df['attendance'].apply(classify_attendance)

# Sort the dataframe based on the attendance category
sorted_df = df.sort_values(by='Attendance Category')

# Display the sorted data
print(sorted_df[['EnrollmentNo', 'StudentName', 'attendance', 'Attendance Category']])
