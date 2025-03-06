import React, { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import SessionList from './components/SessionList';
import { ChatSession } from './types';
import { useAuth } from './hooks/useAuth';
import './styles/App.css';

const App: React.FC = () => {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSession, setCurrentSession] = useState<string | null>(null);
  const { user } = useAuth();

  const createNewSession = () => {
    const newSession: ChatSession = {
      id: `session-${Date.now()}`,
      userId: user?.id,
      messages: [],
      createdAt: new Date(),
      title: `Chat ${sessions.length + 1}`
    };
    setSessions([...sessions, newSession]);
    setCurrentSession(newSession.id);
  };

  const handleSendMessage = async (content: string) => {
    if (!currentSession) return;

    // Add user message
    const userMessage = {
      id: `msg-${Date.now()}`,
      content,
      type: 'user' as const,
      timestamp: new Date()
    };

    // Update session with new message
    const updatedSessions = sessions.map(session => {
      if (session.id === currentSession) {
        return {
          ...session,
          messages: [...session.messages, userMessage]
        };
      }
      return session;
    });
    setSessions(updatedSessions);

    try {
      // Send to backend and get response
      const response = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: content })
      });

      if (!response.ok) throw new Error('Failed to get response');
      
      const data = await response.json();
      
      // Add bot response
      const botMessage = {
        id: `msg-${Date.now()}-bot`,
        content: data.response,
        type: 'bot' as const,
        timestamp: new Date()
      };

      setSessions(prev => prev.map(session => {
        if (session.id === currentSession) {
          return {
            ...session,
            messages: [...session.messages, botMessage]
          };
        }
        return session;
      }));

    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="app-container">
      <aside className="sessions-sidebar">
        <button onClick={createNewSession} className="new-chat-btn">
          New Chat
        </button>
        <SessionList 
          sessions={sessions}
          currentSession={currentSession}
          onSessionSelect={setCurrentSession}
        />
      </aside>
      <main className="chat-main">
        {currentSession ? (
          <ChatWindow
            messages={sessions.find(s => s.id === currentSession)?.messages || []}
            onSendMessage={handleSendMessage}
          />
        ) : (
          <div className="welcome-screen">
            <h1>Welcome to Knowledge Graph Chat</h1>
            <button onClick={createNewSession}>Start a New Chat</button>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
