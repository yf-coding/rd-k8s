import { createServer } from 'http'

var port = 4000

var server = createServer(function (request, response) {
  response.writeHead(200, {'Content-Type': 'text/plain'})
  response.end('Hello World\n')
})

server.listen(port)

console.log('Server running at http://localhost:' + port)