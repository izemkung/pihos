var PythonShell = require('python-shell');

PythonShell.run('DeleteFile.py', function (err,results) {
  if (err) throw err;
  console.log('results: %j', results);
});