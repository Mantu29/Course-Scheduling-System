import pandas as pd
import numpy as np
import itertools
import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt
import seaborn as sns

# Function to process data from Excel files and return processed data frames and dictionaries for further use.
def data_processing(term_1_excelFilePath, term_2_excelFilePath, professor_prefFilePath):
    # Read specified columns from the Excel files for term 1 and term 2
    df1 = pd.read_excel(term_1_excelFilePath, usecols=['Name of the Student', 'Course Title'])
    df2 = pd.read_excel(term_2_excelFilePath, usecols=['Name of the Student', 'Course Title'])
    
    # Combine data from both terms into a single DataFrame
    combined_df = pd.concat([df1, df2], ignore_index=True)
    
    # Group data by student name and aggregate courses into lists
    student_courses = combined_df.groupby('Name of the Student')['Course Title'].apply(list).to_dict()
    # Remove entries where all course values are NaN
    student_courses = {student: courses for student, courses in student_courses.items() if not all(pd.isna(courses))}
    
    # Prepare data for DataFrame creation: list of tuples (student, course)
    data = [(student, course) for student, courses in student_courses.items() for course in courses]
    # Create DataFrame with students and their courses
    student_courses_df = pd.DataFrame(data, columns=['Student', 'Course'])
    
    # Optional: Assign unique numeric identifiers to each student
    student_ids = {name: idx for idx, name in enumerate(student_courses, 1)}
    student_courses_df['Student'] = student_courses_df['Student'].map(student_ids)
    
    # Read professor preferences from Excel
    df_pref = pd.read_excel(professor_prefFilePath)
    # Drop rows where 'Sl. No' is NaN
    df_pref = df_pref.dropna(subset=['Sl. No'])
    
    # Initialize dictionary to store professor preferences
    professor_preferences = {}
    
    # Iterate through each row to populate professor preferences
    for _, row in df_pref.iterrows():
        professor = row.iloc[0]  # Assuming first column contains professor names
        # Initialize preferences for 24 time slots with zero preference
        preferences = {slot: 0 for slot in range(1, 25)}
        
        # Count non-NaN options and assign weights accordingly
        non_nan_options = row[['Option 1', 'Option 2', 'Option 3']].count()
        if non_nan_options == 3:
            weights = {'Option 1': 15, 'Option 2': 10, 'Option 3': 5}
        elif non_nan_options == 2:
            # Different cases based on which options are available
            if pd.notna(row['Option 1']) and pd.notna(row['Option 2']):
                weights = {'Option 1': 30, 'Option 2': 20}
            else:
                weights = {option: 30 for option in ['Option 1', 'Option 2', 'Option 3'] if pd.notna(row[option])}
        else:  # Only one option is not NaN
            weights = {option: 50 for option in ['Option 1', 'Option 2', 'Option 3'] if pd.notna(row[option])}
        
        # Assign weights to preferences based on professor's options
        for option, weight in weights.items():
            if pd.notna(row[option]):
                # Split multiple time slots and assign the same weight
                for slot_str in str(row[option]).split(','):
                    try:
                        slot = int(float(slot_str.strip()))
                        preferences[slot] = weight
                    except ValueError:
                        print(f"Skipping invalid slot value: {slot_str}")

        # Add processed preferences to the dictionary with a unique key for each professor
        professor_preferences[f'P{int(_)+1}'] = preferences
    
    # Prepare data for the DataFrame containing professor preferences
    data_pref = []
    for professor, prefs in professor_preferences.items():
        # Create a row for each professor with their preferences
        row = [prefs[slot] for slot in range(1, 25)]
        row.insert(0, professor)  # Insert professor name at the beginning
        data_pref.append(row)
    
    # Create the DataFrame for professor preferences
    courses_list = list(df_pref['Course list'])
    professor_preferences_df = pd.DataFrame(data_pref, columns=['Professor'] + list(range(1, 25)))
    professor_preferences_df['Course'] = courses_list
    
    return professor_preferences_df, student_courses_df, student_ids, student_courses

# Example usage of the function with file paths
file_path_1 = r"Path\To\Term1.xlsx"
file_path_2 = r"Path\To\Term2.xlsx"
prof_file_path = r"Path\To\ProfessorPreferences.xlsx"

# Function call with example file paths
professor_preferences_df, student_courses_df, student_ids, student_courses = data_processing(file_path_1, file_path_2, prof_file_path)

# List unique courses and define time slots
courses = list(set(professor_preferences_df['Course']))
time_slots = list(range(1, 25))

# Generate classroom names and random capacities
classrooms = ['Classroom_' + str(i) for i in range(1, 7)]
capacities = np.random.randint(15, 20, size=len(classrooms))

# Create DataFrame with classrooms and their capacities
classroom_capacities_df = pd.DataFrame(list(zip(classrooms, capacities)), columns=['Classroom', 'Capacity'])

# Group students per course to get enrollment numbers
students_per_course = student_courses_df.groupby('Course').size().reset_index(name='EnrolledStudents')

# Initialize the Gurobi optimization model for course scheduling
model = gp.Model("Course_Scheduling")

# Decision variables: Binary variables for scheduling courses in classrooms at specific time slots
x = model.addVars([(i, k, t) for i in courses for k in classrooms for t in time_slots], vtype=GRB.BINARY, name="x")

# Constraint: Ensure no student is scheduled for overlapping courses
course_students = student_courses_df.groupby('Course')['Student'].apply(list).to_dict()
for i1, i2 in itertools.combinations(course_students.keys(), 2):
    overlapping_students = set(course_students[i1]) & set(course_students[i2])
    if overlapping_students:
        print(overlapping_students, i1, i2)
        for t in time_slots:
            model.addConstr(gp.quicksum(x[i1, k, t] for k in classrooms) + gp.quicksum(x[i2, k, t] for k in classrooms) <= 1, f"No_Same_Time_Slot_Overlap_{i1}_{i2}_{t}_Constraint")

# Constraints for classroom usage, course scheduling, and professor preferences
for k in classrooms:
    for t in time_slots:
        # Ensure each classroom hosts at most one course per time slot
        model.addConstr(gp.quicksum(x[i, k, t] for i in courses) <= 1, f"Classroom_{k}_Time_{t}_Constraint")

for i in courses:
    # Ensure each course is scheduled exactly once
    model.addConstr(gp.quicksum(x[i, k, t] for k in classrooms for t in time_slots) == 1, f"Course_{i}_Scheduled_Once_Constraint")

for i in courses:
    for t in time_slots:
        # Ensure a course does not occupy more than one classroom at the same time
        model.addConstr(gp.quicksum(x[i, k, t] for k in classrooms) <= 1, f"Single_Classroom_For_Course_{i}_At_Time_{t}_Constraint")

for i in courses:
    for k in classrooms:
        for t in time_slots:
            # Use professor preferences to influence scheduling
            professor = 'P' + str(courses.index(i) + 1)
            preference = professor_preferences_df.loc[professor_preferences_df['Course'] == i, t].values[0]
            model.addConstr(x[i, k, t] <= preference, f"Preference_{i}_{k}_{t}_Constraint")

for i in courses:
    enrolled_students = students_per_course.loc[students_per_course['Course'].str.strip().str.lower() == i.strip().lower(), 'EnrolledStudents'].values[0]
    print(enrolled_students)
    for k in classrooms:
        classroom_capacity = classroom_capacities_df.loc[classroom_capacities_df['Classroom'] == k, 'Capacity'].values[0]
        for t in time_slots:
            # Ensure the number of enrolled students does not exceed classroom capacity
            model.addConstr(x[i, k, t] * enrolled_students <= classroom_capacity, f"Capacity_{i}_{k}_{t}_Constraint")

# Objective: Maximize the sum of professor preference weights for all scheduled courses
model.setObjective(gp.quicksum(x[i, k, t] * professor_preferences_df.loc[professor_preferences_df['Course'] == i, t].values[0] for i in courses for k in classrooms for t in time_slots), GRB.MAXIMIZE)

# Solve the optimization model
model.optimize()

# Prepare to extract the scheduling information if the model has an optimal solution
scheduled_courses = []  # List to store scheduling information

# Check the optimization status
if model.status == GRB.INF_OR_UNBD:
    # Identify conflicting constraints if the model is infeasible or unbounded
    model.computeIIS()  # Identifies the set of conflicting constraints
    model.write("model.ilp")  # Save the infeasibility report
    print("Model is infeasible; the infeasibility report is saved as 'model.ilp'.")
elif model.status == GRB.OPTIMAL:
    # Extract scheduling information for each course if the model has an optimal solution
    for i in courses:
        for k in classrooms:
            for t in time_slots:
                if x[i, k, t].X == 1:  # Check if course i is scheduled in classroom k at time t
                    scheduled_courses.append((i, k, t))
else:
    print(f"Optimization was stopped with status {model.status}")

# Mapping time slots to actual time periods for visualization
time_period_mapping = {
    # Define mappings from numerical time slots to actual time periods
    1: 'Monday 9:30-12:30', 2: 'Monday 2:30-5:30', 3: 'Tuesday 9:30-12:30', 4: 'Tuesday 2:30-5:30',
    5: 'Wednesday 9:30-12:30', 6: 'Wednesday 2:30-5:30', 7: 'Thursday 9:30-12:30', 8: 'Thursday 2:30-5:30',
    9: 'Friday 9:30-12:30', 10: 'Friday 2:30-5:30', 11: 'Saturday 9:30-12:30', 12: 'Saturday 2:30-5:30',
    13: 'Monday-Tuesday 9:30-11:00', 14: 'Monday-Tuesday 11:30-1:00', 15: 'Monday-Tuesday 2:00-3:30',
    16: 'Monday-Tuesday 4:00-5:30', 17: 'Wednesday-Thursday 9:30-11:00', 18: 'Wednesday-Thursday 11:30-1:00',
    19: 'Wednesday-Thursday 2:00-3:30', 20: 'Wednesday-Thursday 4:00-5:30', 21: 'Friday-Saturday 9:30-11:00',
    22: 'Friday-Saturday 11:30-1:00', 23: 'Friday-Saturday 2:00-3:30', 24: 'Friday-Saturday 4:00-5:30'
}

# Create a DataFrame to represent the timetable
timetable = pd.DataFrame(index=classrooms, columns=time_period_mapping.values())

# Populate the timetable DataFrame with scheduled courses
for course, classroom, time_slot in scheduled_courses:
    timetable.at[classroom, time_period_mapping[time_slot]] = course

# Replace NaN with empty strings for a cleaner visual representation
timetable.fillna('', inplace=True)

# Visualize the scheduling using a heatmap
plt.figure(figsize=(50, 30))
sns.heatmap(timetable.notnull(), annot=timetable, fmt='', cmap='viridis', cbar=False)
plt.title('Course Scheduling Visualization')
plt.xlabel('Time Slots')
plt.ylabel('Classrooms')

# Save the heatmap as an image file
plt.savefig('course_scheduling_heatmap.png')
plt.show()

# Export the timetable to a CSV file for further use or analysis
timetable.to_csv('timetable.csv', index=True)
