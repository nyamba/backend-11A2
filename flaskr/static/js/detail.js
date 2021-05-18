
var post_id = $('.reaction').data('postid');

function getCounts() {
	$.get('/reaction/' + post_id, function(data){

		$('.like-count').html(data.like);
		$('.dislike-count').html(data.dislike);

	})
}


getCounts();


$('.btn.like').click(function(){
	var count = 11;
	$.get('/set/like/' + post_id + '/' + count, function(data){
		getCounts();
	})
});

$('.btn.dislike').click(function(){
	getCounts();
});