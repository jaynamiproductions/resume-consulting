function deleteResume(profileid) {
    fetch('/delete-resume', {
    method: 'POST',
    body: JSON.stringify({ profileid: profileid})
    }).then((_res) => {
        window.location.href = "/resume-upload";
    });
}