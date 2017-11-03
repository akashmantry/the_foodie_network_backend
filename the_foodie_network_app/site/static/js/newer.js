function clickAddFriend(data) {
	$.post( "/add/".concat(data), {
	});
	var elem = document.getElementById("addFriend");
	
}

function clickRemoveFriend(data) {
	$.post( "/remove/".concat(data), {

	});
	console.log("/remove/".concat(data))
	console.log("data sent");
}