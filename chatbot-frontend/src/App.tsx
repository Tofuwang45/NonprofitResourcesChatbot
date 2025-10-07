import Chatbot from './components/Chatbot'

export default function App() {
  return (
    <div className="app-root">
      <div className="app-shell">
        <aside className="brand">
          <h1>San Mateo Nonprofit Resources</h1>
          <p className="tag">Natural Language Search for Local Nonprofit Services</p>
          <div className="languages">Supports English & Spanish</div>
          <p className="note">Tip: Press Enter to send, Shift+Enter for newline.</p>
        </aside>

        <section className="panel">
          <Chatbot />
        </section>
      </div>
      <footer className="footer">Built for Nonprofit Search · Local demo</footer>
    </div>
  )
}
