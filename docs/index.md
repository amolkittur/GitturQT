
# Goals and Overview

## Project Purpose

GitturQT is all about making the developer's life easier—because, let’s face it, developers have enough to deal with already. By making Git the main action center for all code development activities, we're giving developers a single source of truth. The goal here is pretty simple: take an idea, put it into a Product Requirements Document (PRD), and then break it down, phase by phase, until it’s something even the most sleep-deprived dev can handle on a daily basis (Red Bull ad).

By the end of each day, the developer should add value to themselves; by the end of each week, add value to their colleagues; and by the end of each month, add value to the world.

GitHub is the home for all these tasks, keeping everything neat, organized, and hopefully reducing the "Wait, what was I supposed to do again?" moments. So yes, we're taking chaos and trying to turn it into something at least resembling a streamlined process.

## Methodology

In today's fast-paced development environment, GitturQT aims to enhance productivity by integrating AI into the typical developer workflow while keeping developers in control at every stage. This Human-in-the-Loop (HIL) approach means that developers can harness the power of AI for routine and complex tasks, but always with the ability to intervene, adjust, and guide the process to align with conscious, value-driven development. Developers are supposed to review consciously at every step along this path; else the product is going to be useless. Below, we outline the lifecycle phases and how HIL AI involvement can make each step more efficient and enjoyable.

## Lifecycle Phases and HIL AI Involvement

### PRD Creation (Once a Month)

- **AI Assistance**: Generating the initial Product Requirements Document by providing template suggestions based on previous projects and industry standards.

- **Essential Ingredients for a Good PRD**:

  1. **PRD Template**: A starting point for your PRD that includes all the necessary sections.
  2. **Meeting Transcription**: The AI transcribes brainstorming sessions, so no idea is left behind. Who has time for typing up notes, anyway?
  3. **Custom Prompt**: The AI uses a personalized prompt that understands your team's unique quirks and preferences (including a love for puns, if that’s your style).

- **Developer Control**: Modify AI-generated suggestions for relevance and accuracy.

### Phase Document (Once a Week)

- **AI Assistance**: Breaking the PRD into specific phases, recommending timelines and dependencies.

- **Requirements for a Phase Document**:

  1. **PRD Doc**: AI takes the existing PRD and extracts the relevant parts.
  2. **Phase Meeting Transcript**: AI captures all the fascinating conversations about timelines and dependencies, complete with those "aha!" moments.
  3. **Custom Prompt**: The AI provides tailored prompts to ensure the phase descriptions aren’t just informative but also entertaining (like comparing phase timelines to running a marathon—slow and steady wins the race).

- **Developer Control**: Adjust phase definitions, timelines, and dependencies to align with project priorities.

### Issue Document (Daily)

- **AI Assistance**: Providing granular daily tasks derived from the weekly phases, helping developers manage daily activities.

- **Components of an Effective Issue Document**:

  1. **Phase Doc**: Using the phase breakdown as a guide.
  2. **Daily Meeting Transcript**: AI transcribes daily stand-ups, capturing all those "we should do this today" moments.
  3. **Custom Prompt**: A special prompt to help break down each task into something manageable, perhaps sprinkled with motivational quotes to keep spirits high ("One bug at a time, my friends").

- **Developer Control**: Refine, add, or remove tasks as needed, allowing for adaptability based on evolving project needs.

### Branch Creation & Commit Messages

- **AI Assistance**: Creating branches and generating commit message templates based on task descriptions.
- **Developer Control**: Retain control over the final commit message, ensuring it aligns with team standards.

### Pull Request (PR) Creation & Review

- **AI Assistance**: Suggesting PR descriptions and conducting preliminary reviews by analyzing code quality and potential issues.
- **Developer Control**: Perform final reviews, make necessary adjustments, and approve the PR.

### Testing & Closing Phases

- **AI Assistance**: Automating test case generation and providing insights into test coverage.
- **Developer Control**: Remain in control of test execution and approve phase closure, maintaining accountability.

This HIL AI-based methodology ensures that developers have granular control at every step of the software development process while leveraging AI to automate routine tasks, provide recommendations, and maintain focus on conscious, value-driven development.

## Development Strategy

### Middle-Out Approach

Let's talk about the middle-out strategy. Imagine you're building a Ferrari—not starting with the flashy paint job (the PRD) or the fancy leather seats (the UI). Nope, we’re diving right into the roaring engine that makes the Ferrari a Ferrari. We're talking about the twin-turbo V8—the part that makes people turn their heads, the part that defines the power and experience. The idea is to focus on the core components that make everything work—simplifying the issue creation process and developing essential AI agents like the audio transcription agent. We’re not here to admire the cup holders or the infotainment system; we’re getting straight to what really matters—the engine that drives everything. Because, at the end of the day, no one's impressed by a Ferrari that looks pretty but doesn’t run.

By starting at the midpoint, we can build outward to connect both ends of the development process. First, we nail down the critical features that will form the backbone of the project. Then, we can circle back to polish the PRD side and add a beautiful interface that makes everything shine. It’s a bit unconventional—sure—but it’s all about developing the features that make a difference. Let's be honest, who needs another meeting template when what we really need is something that works right now!

### In Our Case

In our case, the middle-out approach means starting with the most impactful features that can make developers' lives easier from the get-go. The core features to begin with are:

- **Audio Transcription Agent**: Converts conversations, meetings, and brainstorming sessions into written records without any manual effort. Imagine not needing to scramble for notes during a meeting—just let the AI transcribe everything, ensuring that no idea gets lost.

  **Why**: The Audio Transcription Agent is ranked first because it serves as the foundation for capturing all valuable insights, ideas, and decisions made during discussions. Without clear, accurate notes, the rest of the process can become chaotic. This agent eliminates the burden of note-taking and ensures that no key information is lost, creating a solid basis for everything that follows.

- **Phase Document Generator**: Breaking down the PRD into phases is essential for organizing the workflow. This tool helps structure broad ideas into manageable sections, paving the way for easier implementation.

- **Issue Generation Agent**: Once we have the phases, it's time to break them into daily tasks. This agent ensures that developers know exactly what to focus on each day to keep the project moving forward.

These three components form the backbone of our middle-out development strategy. By focusing on these core agents first, we ensure that developers have a streamlined and efficient workflow. Once these core features are in place, we can expand to enhance the PRD creation, refine the UI, and add other features that will make GitturQT an even more powerful tool.

## Implementation and Deployment

The implementation and deployment of GitturQT involve careful planning to ensure seamless integration, robust functionality, and consistent availability. This section provides a comprehensive overview of the architecture, tools, and processes for setting up and deploying the GitturQT project.

## Architecture Overview

- **Model-View-Controller (MVC)**: GitturQT follows an MVC architecture, ensuring a clear separation of concerns:

  - **Model**: Handles all data-related logic. It represents the core business data, including PRDs, phases, issues, and user settings. It interacts with the database to fetch and save data as required.

  - **View**: The presentation layer, which can be either a PyQT desktop interface or a web interface (final decision pending). It handles user interaction, providing a graphical representation of the data and capturing user inputs.

  - **Controller**: Acts as an intermediary between the Model and View layers. It processes user inputs, communicates with the Model to retrieve data, and then updates the View accordingly.

## Technology Stack

- **Backend**: Python **FastAPI** for building the backend REST APIs. FastAPI is chosen for its asynchronous capabilities, making it highly performant for handling multiple requests, and its intuitive nature makes API development efficient.

- **Frontend**:

  - **PyQT**: Provides a desktop GUI experience, ideal for developers who prefer a local, non-browser-based environment.

  - **Web Interface**: A web-based UI using HTML, CSS, and JavaScript, accessible via any browser. This option is more versatile, allowing for remote access and collaboration.

- **Database**: A SQL database (e.g., PostgreSQL or SQLite) for persistent storage. The Model interacts with the database to store data related to PRDs, phases, issues, and user settings.

- **Server**: Deployed on a macOS server with a static IP address, making it accessible to all team members from various locations.

- **Additional Tools**: *Hakuna Matata* (purpose to be defined).

## Implementation Details

- **Setting Up the Environment**:

  1. **Server Configuration**: Configure the macOS server with all required software installations, such as Python, PostgreSQL, and other dependencies. Enable secure SSH access for remote management.

  2. **Python Virtual Environment**: Use `venv` to create a virtual environment for isolating project dependencies, ensuring no conflicts between different versions of libraries.

  3. **Git Integration**: Clone the project repository onto the server using Git. Ensure all team members have appropriate permissions for branch creation and pushing commits.

- **Backend Development**:

  1. **API Endpoints**: Use FastAPI to create RESTful endpoints for CRUD operations on PRDs, phases, and issues. Document each endpoint clearly for ease of use by the frontend.

  2. **Authentication**: Implement OAuth2 for user authentication to ensure that only authorized users can access and modify project data.

  3. **Database Schema**: Define the database schema for entities like PRD, phases, issues, and users. Use SQLAlchemy to interact with the database.

- **Frontend Development**:

  1. **PyQT Interface**: If a desktop application is preferred, develop the GUI using PyQT. Allow users to create, view, and update PRDs, phases, and issues in a user-friendly way.

  2. **Web Interface**: For a web interface, use a JavaScript framework like Vue.js or React to build a dynamic frontend. This UI should interact with the FastAPI backend to fetch and display data in real-time.

## Deployment Plan

- **Deployment Steps**:

  1. **Set Up Static IP**: Assign a static IP to the macOS server to make it accessible from anywhere. Configure the DNS if needed for easier access.

  2. **Reverse Proxy**: Set up a reverse proxy using Nginx or Apache to direct incoming requests to the appropriate FastAPI port, providing better security and load management.

  3. **SSL Configuration**: Secure communication using an SSL certificate to encrypt all data between the client and the server, ensuring data privacy and integrity.

  4. **Database Migration**: Use Alembic (a tool for managing SQLAlchemy database migrations) to handle database schema changes as the project evolves.

  5. **CI/CD Pipeline**: Set up Continuous Integration/Continuous Deployment pipelines using GitHub Actions. Every push to the main branch should trigger automated tests and, upon passing, automatically deploy the updated code to the server.

## Maintenance and Monitoring

- **Logging and Monitoring**: Implement logging using Python’s `logging` library to track server activity and errors. Use monitoring tools like Prometheus or Grafana to monitor server health, response times, and resource utilization.

- **Backups**: Schedule regular backups of the database to avoid data loss. Store these backups off-site to ensure redundancy.

- **Scalability**: Design the architecture to be scalable. In the event of increased traffic, consider scaling horizontally by adding more servers or vertically by upgrading the current server’s hardware.

- **API Cost Monitoring**: Implement monitoring to keep track of API usage and associated costs.

## Decision Point: Desktop vs Web Interface

- **PyQT Desktop GUI**: Offers a rich desktop experience with advanced GUI elements. Suitable for developers who prefer working locally.

- **Web Interface**: More accessible, ideal for remote teams or situations where users may need to access the tool from multiple devices.

- **Recommendation**: Consider a hybrid approach where a core set of functionalities is available in both formats, allowing users to choose whichever suits their needs best.

