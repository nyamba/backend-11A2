$(function (){

	const Editor = toastui.Editor;

	const editor = new Editor({
	  el: document.querySelector('#editor'),
	  height: '500px',
	  initialEditType: 'wysiwyg',
	});

	console.log('submit button', $('.submit-button'))

	$('.submit-button').on('click', function(evt){
		evt.preventDefault();

		$('#body').val(editor.getMarkdown());
		$('#post-form').submit();

	})

});