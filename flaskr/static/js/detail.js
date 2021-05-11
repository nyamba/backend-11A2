
var post_id = $('.meta').data('postid');
var meta_url = '/meta/'+ post_id;

function get_meta(){
	$.get(meta_url, function(data){
		$('.like').html(data.like);
		$('.dislike').html(data.dislike);
	});
}

get_meta();

$('.action-like').click(function(ent){
	var like_count = parseInt($('.like').html(), 10);
	like_count = like_count + 1;
	var like_url = '/like/'+post_id + '/' + like_count;
	$.get(like_url, function(data){
		get_meta();
	});
});