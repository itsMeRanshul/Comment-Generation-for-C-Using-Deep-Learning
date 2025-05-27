import { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [code, setCode] = useState('');
  const [ast, setAst] = useState('');
  const [comment, setComment] = useState('');

  useEffect(() => {
    const particles = document.createElement("script");
    particles.src = "https://cdn.jsdelivr.net/npm/tsparticles@2.9.3/tsparticles.bundle.min.js";
    particles.onload = () => {
      window.tsParticles.load("tsparticles", {
        fullScreen: { enable: false },
        particles: {
          number: { value: 60 },
          size: { value: 2 },
          move: { enable: true, speed: 0.5 },
          opacity: { value: 0.3 },
          line_linked: { enable: true, distance: 100, color: "#00f0ff", opacity: 0.2 }
        }
      });
    };
    document.body.appendChild(particles);
  }, []);

  const handleGenerate = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/v1/generate', { code });

    setAst(response.data.ast_linear);

    // If response.data.comments is an array of objects
    const formattedComments = response.data.comments
      .map(commentObj => `Block: ${commentObj.block}\nComment: ${commentObj.comment}`)
      .join("\n\n");

    setComment(formattedComments);
  } catch (error) {
    console.error('Error generating comment:', error);
  }
};


  return (
    <div className="relative min-h-screen bg-gradient-to-br from-black via-gray-900 to-gray-800 flex items-center justify-center overflow-hidden">
      <div id="tsparticles" className="absolute top-0 left-0 w-full h-full z-0" />

      <div className="relative z-10 w-11/12 max-w-6xl bg-white/10 backdrop-blur-lg border border-white/20 rounded-3xl shadow-2xl p-10 animate-fade-in">
        <h1 className="text-5xl font-extrabold text-cyan-300 text-center mb-12 tracking-widest uppercase neon-text">
          C Code Comment Generator
        </h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <SectionCard title="Enter Your C Code">
            <textarea
              className="textarea"
              placeholder={`#include <stdio.h>\nint main(void) {\n  // Your code here\n}`}
              value={code}
              onChange={(e) => setCode(e.target.value)}
            ></textarea>
          </SectionCard>

          <SectionCard title="Linearized AST">
            <textarea readOnly className="textarea" value={ast}></textarea>
          </SectionCard>

          <SectionCard title="Generated Comment">
            <textarea readOnly className="textarea" value={comment}></textarea>
          </SectionCard>
        </div>

        <div className="flex justify-center mt-12">
          <button
            onClick={handleGenerate}
            className="relative px-10 py-4 text-lg font-bold text-white bg-gradient-to-r from-cyan-500 to-blue-600 rounded-full shadow-lg hover:scale-105 hover:shadow-cyan-600 transition-transform duration-300 neon-glow focus:outline-none focus:ring-4 focus:ring-cyan-300"
          >
            Generate Comment
            <span className="absolute top-0 left-0 w-full h-full border border-cyan-400 rounded-full animate-ping z-[-1]"></span>
          </button>
        </div>
      </div>
    </div>
  );
}

function SectionCard({ title, children }) {
  return (
    <div className="bg-black/30 backdrop-blur-sm border border-gray-700 rounded-2xl p-6 shadow-lg animate-fade-up">
      <h2 className="text-xl font-semibold text-cyan-100 mb-4 tracking-wide">{title}</h2>
      {children}
    </div>
  );
}

export default App;
