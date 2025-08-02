import datetime

# ------------------ Data Storage ------------------
users = []          # Store all users
tickets = []        # Store all tickets
categories = ["General", "Technical", "Billing"]

# ------------------ Classes -----------------------
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role  # admin / agent / user

class Ticket:
    def __init__(self, ticket_id, user, subject, description, category):
        self.ticket_id = ticket_id
        self.user = user
        self.subject = subject
        self.description = description
        self.category = category
        self.status = "Open"  # Open → In Progress → Resolved → Closed
        self.created_at = datetime.datetime.now()
        self.replies = []
        self.upvotes = 0
        self.downvotes = 0

    def add_reply(self, reply):
        self.replies.append(reply)

# ------------------ Helper Functions ---------------
def authenticate_user(username, password):
    for u in users:
        if u.username == username and u.password == password:
            return u
    return None

def add_ticket(username, subject, description, category):
    ticket_id = len(tickets) + 1
    new_ticket = Ticket(ticket_id, username, subject, description, category)
    tickets.append(new_ticket)

# ------------------ Pre-registered Admin & Agent ---
users.append(User("admin", "admin", "admin"))
users.append(User("agent", "agent", "agent"))
users.append(User("user", "user", "user"))
