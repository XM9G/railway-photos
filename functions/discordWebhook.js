// const axios = require('axios');

// exports.handler = async (event) => {
//   try {
//     // Parse the form data sent from the client
//     const { text, trainType, location, image } = JSON.parse(event.body);

//     // Construct the payload for the Discord webhook
//     const payload = {
//       content: `${text}\nTrain Type: ${trainType}\nLocation: ${location}`,
//       file: image,
//     };

//     // Send a POST request to the Discord webhook URL
//     await axios.post('https://discord.com/api/webhooks/1323101689204707339/VMAMHFU2sZ25Vb2D3rpFFD28JsYidiCsdNgUqF02-LnJ3YPdUn1AUDcA1HmaKjHNXXc-', payload);

//     return {
//       statusCode: 200,
//       body: JSON.stringify({ message: 'Webhook sent successfully' }),
//     };
//   } catch (error) {
//     return {
//       statusCode: 500,
//       body: JSON.stringify({ error: 'Failed to send webhook' }),
//     };
//   }
// };
