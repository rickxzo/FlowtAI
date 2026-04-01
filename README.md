# FlowtAI - Context chatbots made easy.

https://flowtai.onrender.com

## What it does?

Flowt.AI allows the user to create AI agents based on a preset architecture template which allows the agent to access data uploaded by user and respond to queries appropriately.<br>
The entire setup for an agent is only 3 steps
- Specify instruction.
- Choose LLM model.
- Upload context data.

While no mode of topping up is currently implemented, new accounts are **provided with a balance of $0.15**, so feel free to test out.

### Note
The service only provides backend functionality. API to fetch responses is specified in /docs.

## Recent updates -

#### Update 004
- UI redesign for an enhanced experience
- Caching introduced for efficient usage

#### Update 003
- Email verification is now necessary to ensure security. 

#### Update 002
- Conversation short-term context handling is now provided by our service. Read docs for how to use.
- Faster responses.
- Responses are now streamed.
  
#### Update 001
- Cost of initializing an agent is now zero.
- The number of agents per account is now capped at a hundred.
- An initial cost of account creation is to be charged (amount TBD).

## Upcoming updates -
- Improved rate limits
- Faster responses
- Responsive UI

## Stack -
- Flask (Backend framework)
- Vue (Frontend framework)
- TailwindCSS (Styling)
- PostgreSQL - NeonDB (Database)
- Render (Hosting)
- LangGraph (AI agent architecture)
- Redis (Caching)
- https://resend.com (Email sharing)
- https://replicate.com (LLM Inference)
- https://app.pinecone.io (VectorDB)
