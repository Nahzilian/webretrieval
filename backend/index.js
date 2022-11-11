import express from 'express'
import cors from 'cors'
import temp from './temp.json' assert { type: "json" }

const app = express()

// Config
const port = 8000

app.use(cors())
app.use(express.json())

app.get('/', (req, res) => {
    res.send(temp)
})

app.listen(port, () => {
    console.log(`Server running on port ${port}`)
})
