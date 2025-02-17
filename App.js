import { useState } from "react";
import EmotionForm from "./components/EmotionForm";

function App() {
  const [responses, setResponses] = useState([]); // Kullanıcı yanıtlarını saklar

  const handleFormSubmit = (data) => {
    setResponses([...responses, data]);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-5">
      <h1 className="text-2xl font-bold mb-5">Duygu Analizi</h1>
      <EmotionForm onSubmit={handleFormSubmit} />
      
      {/* Kullanıcı Yanıtları */}
      <div className="mt-5 w-full max-w-md bg-white p-4 rounded-lg shadow-md">
        <h2 className="text-lg font-semibold mb-2">Yanıtlar</h2>
        {responses.length === 0 ? (
          <p className="text-gray-500">Henüz yanıt yok.</p>
        ) : (
          <ul className="list-disc pl-5">
            {responses.map((res, index) => (
              <li key={index} className="mb-2">
                <strong>{res.emotion}</strong>: {res.thoughts}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;