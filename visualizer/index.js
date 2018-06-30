/**
 * Created by chamod on 4/29/18.
 */
var express = require('express');
var app = express();
var tweets = require('./tweets');
var aspects = require('./aspects');
var util = require("./util");

const exphbs = require('express-handlebars');

const path = require('path');
const bodyParser = require('body-parser')
const validator = require('express-validator')

app.engine('.hbs', exphbs({
    helpers: {
        equal: function (lvalue, rvalue, options) {
            if (arguments.length < 3)
                throw new Error("Handlebars Helper equal needs 2 parameters")
            if (lvalue != rvalue) {
                return options.inverse(this)
            } else {
                return options.fn(this)
            }
        },
    },
    defaultLayout: 'main',
    extname: '.hbs',
    layoutsDir: path.join(__dirname, 'views/layouts')
}));

const middleware = [
    express.static(path.join(__dirname, '/public')),
    express.static(__dirname + '/node_modules'),
    bodyParser.urlencoded(),
    validator(),
]
app.use(middleware)

app.set('view engine', '.hbs');
app.set('views', './views');

app.use('/tweets', tweets);
app.use('/aspects', aspects);

//home route
app.get('/', function (req, res) {
    util.readJsonFiles().then(function (json_files) {
        res.render('index', {files: json_files, req: req});
    });
});

//unmatched routes(404)
app.get('*', function (req, res) {
    res.send('Sorry, this is an invalid URL.');
});

app.disable('view cache');

app.listen(3000);