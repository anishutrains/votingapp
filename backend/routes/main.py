"""
Main routes for the Voting App.
Contains API endpoints for registration, voting, and statistics.
"""

from flask import Blueprint, jsonify, request, session, render_template
from database.models import (
    get_candidates,
    get_candidate,
    check_voter_voted,
    register_voter,
    record_vote,
    get_vote_statistics
)

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Serve the home page."""
    return render_template('index.html')

@bp.route('/api/candidates', methods=['GET'])
def candidates():
    """Get all candidates."""
    try:
        candidates = get_candidates()
        return jsonify({'success': True, 'candidates': candidates})
    except Exception as e:
        print(f"Error getting candidates: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to get candidates'}), 500

@bp.route('/api/register', methods=['POST'])
def register():
    """Register a new voter."""
    try:
        data = request.get_json()
        name = data.get('name')
        
        if not name:
            return jsonify({'success': False, 'message': 'Name is required'}), 400
            
        # Check if voter has already voted
        if check_voter_voted(name):
            return jsonify({'success': False, 'message': 'You have already voted'}), 400
            
        # Register voter
        voter_id = register_voter(name)
        if not voter_id:
            return jsonify({'success': False, 'message': 'Registration failed'}), 500
            
        # Store voter_id in session
        session['voter_id'] = voter_id
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'voter_id': voter_id
        })
        
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({'success': False, 'message': 'Registration failed'}), 500

@bp.route('/api/vote', methods=['POST'])
def vote():
    """Record a vote for a candidate."""
    try:
        data = request.get_json()
        candidate_id = data.get('candidate_id')
        voter_id = session.get('voter_id')
        
        if not voter_id:
            return jsonify({'success': False, 'message': 'Please register first'}), 400
            
        if not candidate_id:
            return jsonify({'success': False, 'message': 'Candidate ID is required'}), 400
            
        # Record vote
        success = record_vote(voter_id, candidate_id)
        if not success:
            return jsonify({'success': False, 'message': 'Voting failed'}), 500
            
        return jsonify({'success': True, 'message': 'Vote recorded successfully'})
        
    except Exception as e:
        print(f"Voting error: {str(e)}")
        return jsonify({'success': False, 'message': 'Voting failed'}), 500

@bp.route('/api/statistics', methods=['GET'])
def statistics():
    """Get voting statistics."""
    try:
        stats = get_vote_statistics()
        return jsonify({'success': True, 'statistics': stats})
    except Exception as e:
        print(f"Error getting statistics: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to get statistics'}), 500 