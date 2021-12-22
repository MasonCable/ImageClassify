const express = require('express')
const app  = express()
const port = 3000

app.get('/', (req, res) => {
    res.send('This is a test')

    // Load This after the response has been sent back
    console.log('res.data')
})

app.listen(port, () => console.log(`Example app listening on port 
${port}!`))