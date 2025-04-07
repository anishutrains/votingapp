"""
Database models module for the Voting App.

This module contains functions for interacting with the database tables.
"""

from .connection import get_db_connection, execute_query

def get_candidates():
    """Get all candidates from the database"""
    query = "SELECT * FROM candidates"
    return execute_query(query, fetch=True)

def get_candidate(candidate_id):
    """Get a specific candidate by ID"""
    query = "SELECT * FROM candidates WHERE id = %s"
    result = execute_query(query, (candidate_id,), fetch=True)
    return result[0] if result else None

def check_voter_voted(name):
    """Check if a voter has already voted"""
    query = "SELECT has_voted FROM voters WHERE name = %s"
    result = execute_query(query, (name,), fetch=True)
    if result:
        return result[0]['has_voted']
    return None

def register_voter(name):
    """Register a new voter"""
    print(f"Attempting to register voter: {name}")
    
    # Check if voter exists
    query = "SELECT id FROM voters WHERE name = %s"
    result = execute_query(query, (name,), fetch=True)
    
    if result:
        # Voter exists, return their ID
        voter_id = result[0]['id']
        print(f"Voter already exists with ID: {voter_id}")
        return voter_id
    else:
        # Create new voter using direct connection to ensure transaction is committed
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO voters (name, has_voted) VALUES (%s, %s) RETURNING id", (name, False))
            voter_id = cursor.fetchone()[0]
            conn.commit()
            print(f"Created new voter with ID: {voter_id}")
            return voter_id
        except Exception as e:
            conn.rollback()
            print(f"Error creating voter: {e}")
            raise e
        finally:
            conn.close()

def record_vote(voter_id, candidate_id):
    """Record a vote for a candidate"""
    print(f"Attempting to record vote for voter_id: {voter_id}, candidate_id: {candidate_id}")
    
    # Use direct connection to ensure transaction is committed
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Check if voter has already voted
        cursor.execute("SELECT has_voted FROM voters WHERE id = %s", (voter_id,))
        result = cursor.fetchall()
        
        if not result:
            print(f"Voter not found with ID: {voter_id}")
            return False, "Voter not found"
        
        if result[0][0]:  # has_voted is True
            print(f"Voter has already voted: {voter_id}")
            return False, "Voter has already voted"
        
        # Record the vote
        cursor.execute("INSERT INTO votes (voter_id, candidate_id) VALUES (%s, %s)", (voter_id, candidate_id))
        print(f"Vote recorded successfully for voter_id: {voter_id}, candidate_id: {candidate_id}")
        
        # Update voter's has_voted status
        cursor.execute("UPDATE voters SET has_voted = %s WHERE id = %s", (True, voter_id))
        print(f"Updated voter has_voted status to True for voter_id: {voter_id}")
        
        conn.commit()
        return True, "Vote recorded successfully"
    except Exception as e:
        conn.rollback()
        print(f"Error recording vote: {e}")
        return False, f"Error recording vote: {str(e)}"
    finally:
        conn.close()

def get_vote_statistics():
    """Get vote statistics for all candidates"""
    query = """
    SELECT c.name, COUNT(v.id) as votes
    FROM candidates c
    LEFT JOIN votes v ON c.id = v.candidate_id
    GROUP BY c.id, c.name
    ORDER BY votes DESC
    """
    return execute_query(query, fetch=True) 