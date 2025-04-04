from flask import Blueprint, render_template, request, jsonify, session
from app.database import get_candidates, get_candidate, check_voter_voted, register_voter, record_vote, get_vote_statistics, get_db_connection

main = Blueprint('main', __name__)

@main.route('/')
def index():
    candidates = get_candidates()
    return render_template('index.html', candidates=candidates)

@main.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    if not name:
        return jsonify({'success': False, 'message': 'Name is required'})
    
    print(f"Registration attempt for name: {name}")
    
    # Check if voter has already voted
    has_voted = check_voter_voted(name)
    if has_voted:
        print(f"Voter {name} has already voted")
        return jsonify({'success': False, 'message': 'You have already voted'})
    
    try:
        # Register the voter
        voter_id = register_voter(name)
        
        # Verify the voter was created
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, has_voted FROM voters WHERE id = %s", (voter_id,))
        result = cursor.fetchall()
        conn.close()
        
        if result:
            print(f"Verified voter in database: {result}")
        else:
            print(f"WARNING: Voter not found in database after registration: {voter_id}")
        
        session['voter_id'] = voter_id
        session['voter_name'] = name
        print(f"Registered voter: {name} with ID: {voter_id}")
        print(f"Session after registration: {session}")
        return jsonify({'success': True, 'message': 'Registration successful', 'voter_id': voter_id})
    except Exception as e:
        print(f"Error during registration: {e}")
        return jsonify({'success': False, 'message': f'Registration failed: {str(e)}'})

@main.route('/vote', methods=['POST'])
def vote():
    voter_id = session.get('voter_id')
    voter_name = session.get('voter_name')
    print(f"Session when voting: {session}")
    print(f"Voter ID from session: {voter_id}")
    print(f"Voter name from session: {voter_name}")
    
    if not voter_id:
        print("No voter_id in session")
        return jsonify({'success': False, 'message': 'Please register first'})
    
    candidate_id = request.form.get('candidate_id')
    if not candidate_id:
        print("No candidate_id provided")
        return jsonify({'success': False, 'message': 'Candidate ID is required'})
    
    # Convert candidate_id to integer
    candidate_id = int(candidate_id)
    print(f"Recording vote for voter_id: {voter_id}, candidate_id: {candidate_id}")
    
    success, message = record_vote(voter_id, candidate_id)
    
    if success:
        print(f"Vote recorded successfully for {voter_name}")
    else:
        print(f"Failed to record vote: {message}")
    
    return jsonify({'success': success, 'message': message})

@main.route('/statistics')
def statistics():
    stats = get_vote_statistics()
    print(f"Vote statistics: {stats}")
    return jsonify(stats) 