/*const apiKey = 'YOUR_API_KEY'; // Replace with your actual API key
const apiUrl = 'https://api.openai.com/v1/chat/completions'; // Check the OpenAI API documentation for the correct endpoint

const question = document.querySelector('.main-querry');

fetch(apiUrl, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`,
  },
  body: JSON.stringify({
    model: 'gpt-3.5-turbo',
    messages: [
      { role: 'system', content: 'You are a helpful assistant.' },
      { role: 'user', content: question },
    ],
  }),
})
  .then(response => response.json())
  .then(data => {
    // Handle the response data
    document.querySelector('.ans').innerHTML = data;
  })
  .catch(error => {
    // Handle errors
    console.error('Error:', error);
  });*/