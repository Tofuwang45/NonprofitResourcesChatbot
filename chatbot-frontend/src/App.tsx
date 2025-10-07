import Chatbot from './components/Chatbot'

export default function App() {
  return (
    <div className="app-root">
      <div className="app-shell">
        <aside className="brand">
          <h1>Nonprofit Resources</h1>
          <p className="tag">Fast semantic search for local nonprofit services</p>
          <div className="languages">Supports English & Spanish</div>
          <p className="note">Tip: Press Enter to send, Shift+Enter for newline.</p>
        </aside>

        <section className="panel">
          <Chatbot />
        </section>
      </div>
      <footer className="footer">Built for nonprofit discovery · Local demo</footer>
    </div>
  )
}
