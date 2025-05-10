from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure Flask-SQLAlchemy for in-memory SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    configurationId = db.Column(db.String(50), unique=True, nullable=False)
    enabled = db.Column(db.Boolean, default=True)

# Initialize database and seed data
def init_db():
    with app.app_context():
        db.create_all()
        # Seed users
        if not User.query.first():
            admin = User(username='admin', role='admin')
            member = User(username='member', role='member')
            db.session.add_all([admin, member])
        # Seed agents
        if not Agent.query.first():
            gemini = Agent(name='Gemini', configurationId='gemini-pro', enabled=False)
            default_agent = Agent(name='Default', configurationId='default-agent', enabled=True)
            db.session.add_all([gemini, default_agent])
        db.session.commit()

init_db()

# Simulate authentication middleware (simplified)
def get_current_user():
    # In a real app, this would verify JWT or session cookies
    auth_header = request.headers.get('Authorization', 'member')
    user = User.query.filter_by(username=auth_header).first()
    return user.__dict__ if user else None

# Vulnerable endpoint: Allows bypassing agent restrictions
@app.route('/api/assistant/conversations/<conv_id>/messages/<msg_id>/edit', methods=['POST'])
def edit_message_vulnerable(conv_id, msg_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    content = data.get('content', '')
    mentions = data.get('mentions', [])

    # Vulnerability: No validation of configurationId permissions
    for mention in mentions:
        if mention.get('type') == 'agent':
            configuration_id = mention.get('configurationId')
            agent = Agent.query.filter_by(configurationId=configuration_id).first()
            if agent:
                # Simulate chatbot response without checking if agent is enabled
                return jsonify({
                    "message": f"Response from {agent.name}: Hello! You reached {configuration_id}."
                })
            else:
                return jsonify({"error": "Agent not found"}), 404

    return jsonify({"error": "Invalid request"}), 400

# Fixed endpoint: Enforces agent permission checks
@app.route('/api/assistant/conversations/<conv_id>/messages/<msg_id>/edit_fixed', methods=['POST'])
def edit_message_fixed(conv_id, msg_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    content = data.get('content', '')
    mentions = data.get('mentions', [])

    # Fix: Validate agent permissions
    for mention in mentions:
        if mention.get('type') == 'agent':
            configuration_id = mention.get('configurationId')
            agent = Agent.query.filter_by(configurationId=configuration_id, enabled=True).first()
            if agent:
                # Only allow access if agent is enabled
                return jsonify({
                    "message": f"Response from {agent.name}: Hello! You reached {configuration_id}."
                })
            else:
                return jsonify({
                    "error": {
                        "type": "invalid_request_error",
                        "message": "This agent is either disabled or you don't have access to it."
                    }
                }), 403

    return jsonify({"error": "Invalid request"}), 400

# Admin endpoint to manage agents
@app.route('/api/manage_agents', methods=['GET', 'POST'])
def manage_agents():
    user = get_current_user()
    if not user or user['role'] != 'admin':
        return jsonify({"error": "Admin access required"}), 403

    if request.method == 'GET':
        agents = Agent.query.all()
        return jsonify([{
            'id': agent.id,
            'name': agent.name,
            'configurationId': agent.configurationId,
            'enabled': agent.enabled
        } for agent in agents])

    if request.method == 'POST':
        data = request.get_json()
        agent_id = data.get('id')
        enabled = data.get('enabled')
        agent = Agent.query.get(agent_id)
        if agent:
            agent.enabled = enabled
            db.session.commit()
            return jsonify({"message": "Agent updated"})
        return jsonify({"error": "Agent not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)