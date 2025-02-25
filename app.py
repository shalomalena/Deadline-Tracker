from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)


deadlines = []

todos = []

@app.route('/')
def index():
    
    today = datetime.today()

   
    todos.clear()  
    for deadline in deadlines:
        if 'plan' in deadline and deadline['plan'] is not None:
            plan = deadline['plan']
            start_date = plan['start_date']
            submit_date = plan['submit_date']
            frequency = plan['frequency']
            hours = plan['hours']
            custom_days = plan.get('custom_days', [])
            
            current_date = start_date
            while current_date <= submit_date:
                if frequency == 'daily':
                    todos.append({
                        'date': current_date,
                        'company_name': deadline['company_name'],
                        'hours': hours
                    })
                    current_date += timedelta(days=1)
                elif frequency == 'every_two_days':
                    todos.append({
                        'date': current_date,
                        'company_name': deadline['company_name'],
                        'hours': hours
                    })
                    current_date += timedelta(days=2)
                elif frequency == 'weekends' and current_date.weekday() >= 5:  # Saturday or Sunday
                    todos.append({
                        'date': current_date,
                        'company_name': deadline['company_name'],
                        'hours': hours
                    })
                    current_date += timedelta(days=1)
                elif frequency == 'custom' and current_date.strftime('%A') in custom_days:
                    todos.append({
                        'date': current_date,
                        'company_name': deadline['company_name'],
                        'hours': hours
                    })
                    current_date += timedelta(days=1)
                else:
                    current_date += timedelta(days=1)
    
    return render_template('index.html', todos=todos)

@app.route('/update-todo', methods=['POST'])

def update_todo():
    global todos  

    # Get the indices of the tasks that were marked as completed
    completed_tasks = request.form.getlist('completed')

    # Convert indices to integers and remove them from the to-do list
    for completed in completed_tasks:
        index = int(completed)
        if index < len(todos): 
            todos.pop(index)

    return redirect(url_for('index'))

    

# Add Deadline
@app.route('/add-deadline', methods=['GET', 'POST'])
def add_deadline():
    if request.method == 'POST':
        # Capture form data
        application_type = request.form['application_type']
        company_name = request.form['company_name']
        deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d')
        link = request.form.get('link')
        description = request.form.get('description')
        status = request.form['status']

        # Add the new deadline to the in-memory list
        deadlines.append({
            'application_type': application_type,
            'company_name': company_name,
            'deadline': deadline,
            'link': link,
            'description': description,
            'status': status,
            'plan': None  
        })

      
        return redirect(url_for('view_deadlines'))

    return render_template('add_deadline.html')

# View Deadlines 
@app.route('/view-deadlines')
def view_deadlines():
    # Sort deadlines by date (earliest at the top)
    active_deadlines = [deadline for deadline in deadlines if deadline['status'] != 'Submitted']
    return render_template('view_deadlines.html', deadlines=active_deadlines)



@app.route('/submit-application/<int:index>', methods=['POST'])
def submit_application(index):
    # Update the status to "Submitted"
    deadlines[index]['status'] = 'Submitted'

    # Remove the associated tasks from the todos list
    global todos
    todos = [task for task in todos if task['company_name'] != deadlines[index]['company_name']]

    # Redirect to the view deadline page
    return redirect(url_for('view_deadlines'))


#  viewing submitted applications

@app.route('/submitted-applications')
def submitted_applications():
    # Filter submitted applications
    submitted = [app for app in deadlines if app['status'] == 'Submitted']
    return render_template('submitted_applications.html', applications=submitted)



#  viewing applications in the My Plan section
@app.route('/my-plan')
def my_plan():
    # Show the list of applications without plans
    active_plans = [app for app in deadlines if app['status'] != 'Submitted']
    return render_template('my_plan.html', deadlines=active_plans)
    

# adding a plan to an application
@app.route('/add-plan/<int:index>', methods=['GET', 'POST'], endpoint='add_plan_with_index')
def add_plan_with_index(index):
    deadline = deadlines[index]
    today = datetime.today()

    if request.method == 'POST':
        # Capture the plan details
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        submit_date = datetime.strptime(request.form['submit_date'], '%Y-%m-%d')
        frequency = request.form['frequency']
        custom_days = request.form.getlist('custom_days')  # Get custom days if selected
        hours = request.form.get('hours')

        # Save the plan in the deadline
        deadline['plan'] = {
            'start_date': start_date,
            'submit_date': submit_date,
            'frequency': frequency,
            'hours': hours,
            'custom_days': custom_days  # Save selected custom days
        }

        return redirect(url_for('my_plan'))

    # Calculate how many days are left
    days_left = (deadline['deadline'] - today).days
    return render_template('add_plan.html', deadline=deadline, days_left=days_left)



# to add a plan (if this is a different one, you can clarify its purpose)
@app.route('/add-plan-simple/<int:index>', methods=['GET', 'POST'])
def add_plan_simple(index):
    if request.method == 'POST':
        plan = request.form['plan']
        deadlines[index]['plan'] = plan
        return redirect(url_for('view_deadlines'))

    return render_template('add_plan_simple.html', index=index)




if __name__ == '__main__':
    app.run(debug=True)
