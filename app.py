from app import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'low' not in session:
        session['low'] = 1
        session['high'] = 100
        session['guess'] = None

    message = ''
    if request.method == 'POST':
        feedback = request.form.get('feedback')
        
        if feedback == 'correct':
            message = f"I guessed it! Your number is {session['guess']}."
            session.clear()
        else:
            guess = session.get('guess')
            if feedback == 'high':
                session['high'] = guess - 1
            elif feedback == 'low':
                session['low'] = guess + 1
            
            if session['low'] > session['high']:
                message = "Hmm, inconsistent feedback! Let's start over."
                session.clear()
                return redirect(url_for('home'))

            session['guess'] = (session['low'] + session['high']) // 2
            message = f"Is your number {session['guess']}?"
    else:
        session['guess'] = (session['low'] + session['high']) // 2
        message = f"Think of a number between 1 and 100. Is it {session['guess']}?"

    return render_template('index.html', message=message)
