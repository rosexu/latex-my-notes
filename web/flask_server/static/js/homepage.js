/**
 * Created by rosexu on 15-09-13.
 */
$(document).ready (function() {
    test();
});


function test()
{
    console.log('hi');
    $.ajax({
    async: false,
    type: "GET",
    url: 'all',
    success: function(msg){
        console.log(msg.results)
        var titles = []
        for (i=0; i< msg.results.length; i++) {
            dbObj = msg.results[i];
            title = dbObj.title;
            console.log(title);
            titles.push(title)
        }

        var start = '<a href="/static/static/';
        var middle = '.pdf"><div class="document"><h1>';
        var end = '</h1></div></a>';
        var thing = '';

        for (i = 0; i<titles.length; i++) {
            console.log(titles[i]);
            var title = titles[i];
            thing = thing + start;
            thing = thing + title;
            thing = thing + middle;
            thing = thing + title;
            thing = thing + end;
        }

        console.log($('.results'));
        $('.results').html(thing);
    }
    });
}