# Deadline Tracker

The Deadline Tracker is a web-based application designed to help users manage deadlines for various applications such as internships, scholarships, fellowships, research projects, and more. The platform allows users to keep track of important dates, create personalized work plans, and visualize their schedule in an intuitive to-do list format.

[View the design on Figma](https://www.figma.com/board/wC9ZP1rSBn1FtRvdCiXoGf/Deadline-Tracker?node-id=0-1&t=gnJhXN4boU98cgyK-1)

## Features

- **Add Deadlines**: Users can add deadlines for different types of applications. Each deadline includes details such as the company/program name, a description, a link, and the deadline date.
- **View Deadlines**: Deadlines are displayed in an ordered table with the nearest deadlines at the top, helping users prioritize their tasks effectively.
- **Submit Status**: Once a user has completed and submitted an application, they can mark it as "Submitted," removing it from the active deadlines list and moving it to a "Submitted Applications" section.
- **Create Work Plans**: Users can create detailed work plans for each application, specifying their start date, submission date, frequency of work (daily, every two days, weekends, or custom), and the number of hours they plan to work each day.
- **To-Do List**: The application automatically generates a to-do list based on the user’s work plan, displaying tasks day-by-day. Users can check off tasks as they complete them, and checked tasks will be displayed with a strikethrough.

## How It Works

- **Adding a Deadline**: Users can input details such as the application type (internship, scholarship, etc.), company/program name, deadline date, link, and description.
- **Planning Work**: Users can create custom work schedules by selecting start and submission dates and how often they plan to work on each application. The system calculates the days left to work and organizes the user's tasks.
- **Managing Tasks**: The to-do list is populated with tasks based on the work plan, allowing users to easily keep track of what needs to be done and when. Tasks are displayed by date, and users can mark them as complete.

## Tech Stack

- **Flask**: Python web framework used for developing the application backend.
- **Flask-SQLAlchemy**: ORM used to manage the application's database.
- **HTML/CSS**: Used for the front-end interface, providing a clean and user-friendly experience.
- **JavaScript**: Dynamically handles task completion in the to-do list.
- **SQLite**: Lightweight database for storing application data.
