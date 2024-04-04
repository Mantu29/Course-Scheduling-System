# Course-Scheduling-System
This course scheduling system is designed to automate the creation of academic schedules, taking into account professor preferences, student course registrations, and classroom capacities.

\section*{Overview}
This course scheduling system is designed to automate the creation of academic schedules, taking into account professor preferences, student course registrations, and classroom capacities. It aims to optimize the allocation of courses to timeslots and classrooms, ensuring that no student is double-booked and that professors' time slot preferences are respected as much as possible.

\section*{Dataset Formats}
The system requires three main datasets in Excel format:

\subsection*{1. Term Course Registrations}
Each term's course registration data should be provided in separate Excel files with the following columns:
\begin{itemize}
    \item \textbf{Name of the Student}: The full name of the student.
    \item \textbf{Course Title}: The title of the course for which the student has registered.
\end{itemize}

Example for "Term 2 Course Registration":
\begin{longtable}[c]{|p{3cm}|p{4cm}|}
    \hline
    \textbf{Name of the Student} & \textbf{Course Title} \\
    \hline
    John Doe & Introduction to AI \\
    Jane Smith & Advanced Robotics \\
    \dots & \dots \\
    \hline
\end{longtable}

\subsection*{2. Professor Preferences}
The professor preferences should be provided in an Excel file with the following columns:
\begin{itemize}
    \item \textbf{Sl. No}: A serial number for each entry.
    \item \textbf{Professor Name}: The full name of the professor.
    \item \textbf{Course list}: The titles of courses the professor is willing to teach.
    \item \textbf{Option 1}, \textbf{Option 2}, \textbf{Option 3}: Professor's preferred time slots, ranked from most to least preferred. Time slots should be represented by integers (e.g., 1 for 'Monday 9:30-12:30', 2 for 'Monday 2:30-5:30', etc.).
\end{itemize}

Example for "Professor Preferences":
\begin{longtable}[c]{|p{1cm}|p{3cm}|p{3cm}|p{2cm}|p{2cm}|p{2cm}|}
    \hline
    \textbf{Sl. No} & \textbf{Professor Name} & \textbf{Course list} & \textbf{Option 1} & \textbf{Option 2} & \textbf{Option 3} \\
    \hline
    1 & Dr. Alice & Introduction to AI & 1, 2 & 3, 4 & 5 \\
    2 & Dr. Bob & Advanced Robotics & 2, 3 & 1, 4 & 6 \\
    \dots & \dots & \dots & \dots & \dots & \dots \\
    \hline
\end{longtable}

\subsection*{3. Classroom Capacities (Optional)}
If classroom capacity needs to be considered, an additional dataset might be required with the following structure:
\begin{itemize}
    \item \textbf{Classroom Name}: The name or identifier of the classroom.
    \item \textbf{Capacity}: The maximum number of students that can be accommodated.
\end{itemize}

Example for "Classroom Capacities":
\begin{longtable}[c]{|p{3cm}|p{3cm}|}
    \hline
    \textbf{Classroom Name} & \textbf{Capacity} \\
    \hline
    Room 101 & 30 \\
    Room 102 & 25 \\
    \dots & \dots \\
    \hline
\end{longtable}

\section*{Getting Started}
\begin{itemize}
    \item Ensure that all required datasets are prepared according to the specified formats.
    \item Update the file paths in the code to point to your datasets.
    \item Run the scheduling system to generate the course schedules.
\end{itemize}

\section*{Dependencies}
Install all required dependencies using the \texttt{requirements.txt} file provided in the project:
\begin{verbatim}
pip install -r requirements.txt
\end{verbatim}

\section*{Contribution}
Contributions to the project are welcome. Please follow the standard fork-pull request workflow.

\section*{License}
This project is licensed under [License Name]. See the LICENSE file for more details.

\end{document}
