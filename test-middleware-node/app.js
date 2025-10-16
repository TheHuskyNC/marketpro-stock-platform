const express = require('express');
const loggerMiddleware = require('./loggerMiddleware');

const app = express();
app.use(loggerMiddleware);

app.get('/', (req, res) => {
    res.send('Success');
});

const PORT = 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
