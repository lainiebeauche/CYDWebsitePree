from database import (
    is_username_taken, add_user, authenticate, get_user_from_database,
    get_all_messages, add_message, delete_all_messages
)
from flask import (
    Flask, redirect, render_template, request, session, url_for, flash
)

APP = Flask(__name__)
#APP.config['SECRET_KEY'] = 'super-secret-key'


AFFIRMATIONS = [
    "I feel the love of those who are not physically around me",
    "I take pleasure in my own solitude",
    "I am too big of a gift to this world to feel self-pity",
    "I love and approve of myself",
    "I am focusing on breathing and grounding myself",
    "Following my intuition and my heart keeps me safe and sound",
    "I make the right choices every time",
    "I draw from me inner strength and light",
    "I trust myself",
    "I am a unique child of this world",
    "I have as much brightness to offer the world as the next person",
    "I matter and what I have to offer this world also matters",
    "I trust me inner wisdom and intuition",
    "I breathe in calmness and breathe out nervousness",
    "This situation works out for me highest good",
    "Wonderful things unfold before me",
    "I forgive myself for all the mistakes I have made",
    "I let go of me anger so I can see clearly",
    "I accept responsibility if me anger has hurt anyone",
    "I replace me anger with understanding and compassion",
    "I offer an apology to those affected by me anger",
    "I may not understand the good in this situation but it is there",
    "I muster up more hope and courage from deep inside me",
    "I choose to find hopeful and optimistic ways to look at this",
    "I kindly ask for help and guidance if I cannot see a better way",
    "I refuse to give up because I haven't tried all possible ways",
    "I know me wisdom guides me to the right decision",
    "I trust myself to make the best decision for me",
    "I receive all feedback with kindness but make the final call myself",
    "I listen lovingly to this inner conflict and reflect on it until I get to peace around it",
    "I love me family even if they do not understand me completely",
    "I show me family how much I love them in all the verbal and non-verbal ways I can",
    "There is a good reason I was paired with this perfect family",
    "I choose to see me family as a gift",
    "I am a better person from the hardship that I've gone through with me family",
    "I choose friends who approve of me and love me",
    "I surround myself with people who treat me well",
    "I take the time to show me friends that I care about them",
    "me friends do not judge me, nor do they influence what I do with me life",
    "I take great pleasure in me friends, even if they disagree or live different lives",
    "I am beautiful and smart and that's how everyone sees me",
    "I take comfort in the fact that I can always leave this situation",
    "I never know what amazing incredible person I will meet next",
    "The company of strangers teaches me more about me own likes and dislikes",
    "I am doing work that I enjoy and find fulfilling",
    "I play a big role in me own career success",
    "I ask for and do meaningful, wonderful and rewarding work",
    "I engage in work that impacts this world positively",
    "I believe in me ability to change the world with the work that I do",
    "Peaceful sleep awaits me in dreamland",
    "I let go of all the false stories I make up in me head",
    "I release me mind of thought until the morning",
    "I embrace the peace and quiet of the night",
    "I sleep soundly and deeply and beautifully into this night",
    "This day brings me nothing but joy",
    "Today will be a gorgeous day to remember",
    "me thoughts are me reality so I think up a bright new day",
    "I fill me day with hope and face it with joy",
    "I choose to fully participate in me day",
    "I let go of worries that drain me energy",
    "I make smart, calculated plans for me future",
    "I am a money magnet and attract wealth and abundance",
    "I am in complete charge of planning for me future",
    "I trust in me own ability to provide well for me family",
    "I follow me dreams no matter what",
    "I show compassion in helping me loved ones understand me dreams",
    "I ask me loved ones to support me dreams",
    "I answer questions about me dreams without getting defensive",
    "me loved ones love me even without fully grappling with me dreams",
    "I accept everyone as they are and continue on with pursuing me dream",
    "I am safe and sound. All is well",
    "Everything works out for me highest good",
    "There is a great reason this is unfolding before me now",
    "I have the smarts and the ability to get through this",
    "All me problems have a solution",
    "I attempt all - not some - possible ways to get unstuck",
    "I seek a new way of thinking about this situation",
    "The answer is right before me, even if I am not seeing it yet",
    "I believe in me ability to unlock the way and set myself free",
    "I have no right to compare myself to anyone for I do not know their whole story",
    "I compare myself only to me highest self",
    "I choose to see the light that I am to this world",
    "I am happy in me own skin and in me own circumstances",
    "I see myself as a gift to me people and community and world",
    "I am more than good enough and I get better every day",
    "I give up the habit of criticising myself",
    "I adopt the mindset of praising myself",
    "I see the perfection in all me flaws and all me genius",
    "I fully approve of who I am, even as I get better",
    "I am a good person at all times of day and night",
    "I cannot give up until I have tried every conceivable way",
    "Giving up is easy and always an option so let's delay it for another day",
    "I press on because I believe in me path",
    "It is always too early to give up on me goals",
    "I must know what awaits me at the end of this rope so I do not give up",
    "The past has no power over me anymore. I embrace the rhythm and the flowing of me own heart",
    "All that I need comes to me at the right time and place in this life",
    "I am deeply fulfilled with who I am."
]


@APP.route('/navbar')
def navbar():
    """Render the navbar.

    Since the navbar is always the same, no logic is needed: we can render it
    and return it right away.

    """
    return render_template('navbar.html', session=session)


@APP.route('/')
def home():
    """Render the homepage.

    Since the homepage is always the same, no logic is needed: we can render it
    and return it right away.

    """
    return render_template('home.html')

@APP.route('/blog')
def blog():
    return render_template('blog.html')

@APP.route('/signup', methods=['POST', 'GET'])
def signup():
    """Render the signup page.

    There are two ways to interact with the signup page: with a GET request or
    a POST request. A GET request just loads the signup page for the user to
    fill out. But when the user submits the signup form, their info is sent
    to the same URL as a POST request. (Think of it like mail: a GET request
    is like asking someone to send you a letter so you can GET it from your
    mailbox, and a POST request is like sending a letter using POSTage.) This
    function needs to handle both cases.

    Args:
        message (str): a message to display on the signup page (for errors).

    """
    # We need to do different things depending on whether the request is GET
    # or POST, so we check to see which one it is before we go any further.
    if request.method == 'GET':
        # Show the user the login page
        return render_template("signup.html", session=session)
    else:
        # The user is sending their data to sign up. We can now read their
        # information from a dictionary contained within the request, in the
        # attribute `request.form`.
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        user_bio = request.form['user_bio']
        # Check to see if their desired username is taken
        if is_username_taken(username):
            # We will now reload the page with a message
            flash("Username already taken; please choose a different one.")
            """`flash` stores this message exclusively for the next request,
            which we immediately initiate using `redirect`. When the template
            loads, it checks for the presence of any flashed messages, and
            displays them as errors if so. (See `signup.html` and the included
            template `errors.html`.)
            """
            return redirect(url_for('signup'))

        """Since the line above has a `return` statement, execution of the
        function ends here: if the username was taken, nothing below this line
        will run. This means we can now assume that the username is available.
        """
        # Add user information to database
        add_user(name, username, password, age, user_bio)

        # Save user to session and redirect to their Profile
        session['username'] = username
        return redirect(url_for('profile'))


@APP.route('/login', methods=['POST', 'GET'])
def login():
    """Render the login page.

    As with the signup page, there are two ways to interact with the login
    page: either by loading the page the first time (GET) or sending the
    credentials for authentication (POST).

    """
    if request.method == 'GET':
        # show the user the login page
        return render_template("login.html", session=session)
    else:
        # the user is trying to log in
        username = request.form['username']
        password = request.form['password']
        if authenticate(username, password):
            # save user to session and redirect to their Profile
            session['username'] = username
            return redirect('/profile')
        # failed login, redirect to login page
        flash("Wrong username or password. Try again.")
        return redirect(url_for('login'))


@APP.route('/profile')
def profile():
    """Render the user's profile."""
    if 'username' in session:
        # if the user is logged in (a.k.a. in session)
        username = session['username']
        user = get_user_from_database(username)
        return render_template('profile.html', user=user)
    # user is not yet logged in
    message = "You must login to access your Profile."
    return render_template("login.html", message=message)


@APP.route('/logout')
def logout():
    """Remove the session from the browser."""
    try:
        session.pop('username')
    except KeyError:
        pass
    return redirect('/login')


@APP.route('/chillzone')
def chillzone():
    """Render the chill zone."""
    puppy_number = int(request.args.get('puppy_number', 0))
    puppy_number = puppy_number % 24
    affirmation_number = int(request.args.get('affirmation_number', 0))
    affirmation_number = affirmation_number % len(AFFIRMATIONS)
    affirmation = AFFIRMATIONS[affirmation_number]
    return render_template(
        'chillzone.html',
        puppy_number=puppy_number,
        affirmation_number=affirmation_number,
        affirmation=affirmation
    )


@APP.route('/chillzone/puppy/<puppy_number>')
def puppy(puppy_number):
    """Render a specific puppy page."""
    return render_template('puppy.html', puppy_number=puppy_number)


@APP.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')

@APP.route('/resource')
def resource():
    """Render the about page."""
    return render_template('resources.html')

@APP.route('/pep')
def pep():
    """Render the pep page."""
    return render_template('pep.html')

@APP.route('/delete_all')
def delete_all():
    delete_all_messages()
    return render_template('messages.html', messages=get_all_messages(), session='username' in session)

@APP.route('/messages', methods=['GET', 'POST'])
def messages():
    print(session)
    print('username' in session)
    """Render the messages page (GET) or create a message (POST)."""
    if 'username' in session:
        username = session['username']
        user = get_user_from_database(username)
    else:
        user = None

    if request.method == 'POST':
        # This request is adding a new message from a logged-in user
        text = request.form['text']
        username = request.form['username']
        add_message(username, text)

    # Regardless of whether the request was GET or POST, we render the page
    # with all messages.
    return render_template(
        'messages.html',
        messages=get_all_messages(),
        user=user,
        session='username' in session
    )


if __name__ == "__main__":
    APP.run(port=8000, debug=True)
