# Course-Scheduling-System
This course scheduling system is designed to automate the creation of academic schedules, taking into account professor preferences, student course registrations, and classroom capacities.

# Course Scheduling System

## Overview
This course scheduling system is designed to automate the creation of academic schedules, taking into account professor preferences, student course registrations, and classroom capacities. It aims to optimize the allocation of courses to timeslots and classrooms, ensuring that no student is double-booked and that professors' time slot preferences are respected as much as possible.

## Dataset Formats
The system requires three main datasets in Excel format:

### 1. **Term Course Registrations**
Each term's course registration data should be provided in separate Excel files with the following columns:
- `Name of the Student`: The full name of the student.
- `Course Title`: The title of the course for which the student has registered.

Example for "Term 2 Course Registration":
| Name of the Student | Course Title       |
|---------------------|--------------------|
| John Doe            | Introduction to AI |
| Jane Smith          | Advanced Robotics  |
| ...                 | ...                |

### 2. **Professor Preferences**
The professor preferences should be provided in an Excel file with the following columns:
- `Sl. No`: A serial number for each entry.
- `Professor Name`: The full name of the professor.
- `Course list`: The titles of courses the professor is willing to teach.
- `Option 1`, `Option 2`, `Option 3`: Professor's preferred time slots, ranked from most to least preferred. Time slots should be represented by integers (e.g., 1 for 'Monday 9:30-12:30', 2 for 'Monday 2:30-5:30', etc.).

Example for "Professor Preferences":
| Sl. No | Professor Name | Course list       | Option 1 | Option 2 | Option 3 |
|--------|----------------|-------------------|----------|----------|----------|
| 1      | Dr. Alice      | Introduction to AI| 1        | 3        | 5        |
| 2      | Dr. Bob        | Advanced Robotics | 2        | 1        | 6        |
| ...    | ...            | ...               | ...      | ...      | ...      |

### 3. **Classroom Capacities** (Optional)
If classroom capacity needs to be considered, an additional dataset might be required with the following structure:
- `Classroom Name`: The name or identifier of the classroom.
- `Capacity`: The maximum number of students that can be accommodated.

Example for "Classroom Capacities":
| Classroom Name | Capacity |
|----------------|----------|
| Room 101       | 30       |
| Room 102       | 25       |
| ...            | ...      |

## Mathematical Formulation

### Objective Function
Maximize the total preference score of professors for assigned time slots and classrooms for their courses, ensuring an optimal schedule that respects professor preferences as much as possible.

### Decision Variables
`x_{i,k,t}`: Binary variable that is 1 if course `i` is scheduled in classroom `k` during time slot `t`, and 0 otherwise.

### Constraints

1. **No Overlapping Courses for Students:**
   For any two courses `i_1` and `i_2` with common students, they cannot be scheduled at the same time.

∑_{k} x_{i_1,k,t} + ∑_{k} x_{i_2,k,t} ≤ 1 ∀ t, if i_1 and i_2 have common students


2. **Single Course per Classroom per Time Slot:**
Each classroom can host at most one course at any time slot.

∑_{i} x_{i,k,t} ≤ 1 ∀ k, ∀ t


3. **Course Scheduling:**
Each course must be scheduled exactly once during the planning period.

∑_{k}∑_{t} x_{i,k,t} = 1 ∀ i


4. **Professor Preferences:**
A course can only be scheduled in a time slot if the professor's preference for that slot is not zero.

x_{i,k,t} ≤ preference of professor for course i at time t ∀ i, ∀ k, ∀ t


5. **Classroom Capacity:**
The number of students enrolled in a course cannot exceed the capacity of the assigned classroom.
x_{i,k,t} * enrolled students in course i ≤ capacity of classroom k ∀ i, ∀ k, ∀ t


### Variables
- `i`: Index for courses.
- `k`: Index for classrooms.
- `t`: Index for time slots.


## Getting Started
- Ensure that all required datasets are prepared according to the specified formats.
- Update the file paths in the code to point to your datasets.
- Run the scheduling system to generate the course schedules.

## Dependencies
Install all required dependencies using the `requirements.txt` file provided in the project:
