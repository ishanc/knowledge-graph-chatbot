export interface Message {
  id: string;
  content: string;
  type: 'user' | 'bot';
  timestamp: Date;
}

export interface ChatSession {
  id: string;
  userId?: string;
  title: string;
  messages: Message[];
  createdAt: Date;
}

export interface User {
  id: string;
  name: string;
  email: string;
}
