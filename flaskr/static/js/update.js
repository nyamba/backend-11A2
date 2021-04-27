$(function(){

	const Editor = toastui.Editor;

	const editor = new Editor({
	  el: document.querySelector('#editor'),
	  height: '500px',
	  initialEditType: 'wysiwyg',
	  initialValue: $('#body').val()
	});

	$('.submit').click(function(evt) {
		evt.preventDefault();

		$('#body').val(editor.getMarkdown());
		$('#update-form').submit();
	});

})