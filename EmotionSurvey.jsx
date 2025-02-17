import { useState } from "react";

const EmotionSurvey = ({ onSubmit }) => {
  const [emotion, setEmotion] = useState(""); // Seçilen duygu
  const [thoughts, setThoughts] = useState(""); // Açık uçlu yanıt

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ emotion, thoughts });
    setEmotion("");
    setThoughts("");
  };

  return (
    <div className="p-4 max-w-md mx-auto bg-white shadow-lg rounded-lg">
      <h2 className="text-xl font-semibold mb-4">Bugün Nasıl Hissediyorsun?</h2>
      
      {/* Duygu Seçimi */}
      <select 
        value={emotion} 
        onChange={(e) => setEmotion(e.target.value)} 
        className="w-full p-2 border rounded-md mb-3"
      >
        <option value="">Duygu Seç</option>
        <option value="Mutlu">Mutlu 😊</option>
        <option value="Üzgün">Üzgün 😢</option>
        <option value="Stresli">Stresli 😰</option>
        <option value="Motivasyonlu">Motivasyonlu 💪</option>
        <option value="Yorgun">Yorgun 😴</option>
      </select>

      {/* Açık Uçlu Yanıt */}
      <textarea
        value={thoughts}
        onChange={(e) => setThoughts(e.target.value)}
        placeholder="Bugün nasıl hissettiğini anlatabilirsin..."
        className="w-full p-2 border rounded-md mb-3"
        rows="4"
      />

      {/* Gönder Butonu */}
      <button 
        onClick={handleSubmit} 
        className="w-full bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600"
      >
        Gönder
      </button>
    </div>
  );
};

export default EmotionSurvey;