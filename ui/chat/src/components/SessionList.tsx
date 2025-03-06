import React from 'react';
import { ChatSession } from '../types';

interface SessionListProps {
  sessions: ChatSession[];
  currentSession: string | null;
  onSessionSelect: (sessionId: string) => void;
}

const SessionList: React.FC<SessionListProps> = ({ 
  sessions, 
  currentSession, 
  onSessionSelect 
}) => {
  return (
    <div className="sessions-list">
      {sessions.map(session => (
        <div
          key={session.id}
          className={`session-item ${currentSession === session.id ? 'active' : ''}`}
          onClick={() => onSessionSelect(session.id)}
        >
          <div className="session-title">{session.title}</div>
          <div className="session-date">
            {new Date(session.createdAt).toLocaleDateString()}
          </div>
        </div>
      ))}
    </div>
  );
};

export default SessionList;
