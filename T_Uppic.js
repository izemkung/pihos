var PythonShell = require('python-shell');

var isError = 0;

PythonShell.run('newPic.py', function (err) 
{
  if (err)
  { 
    console.log(err);
  }
  console.log('Error Up Pic');
});

