// wew select each row and add the subjects color to that row. 
// , lets try that.

// we find the subject selected, find that out. 
// once we've done that, we need to reaload the table.
// We should select all of the rows, remove the irrelevant ones.
// Take the editied list and append them all to the table.




let selectedSubject = document.querySelector('#subject-dropdown');
let taskList = {{ tasks|tojson }}
selectedSubject.addEventListener('change', () => {
    let value = selectedSubject.value;


})
let value = selectedSubject.value;


// we want the dropwdown to work when we select a spevific subject, to then only display tasks for that subject.
// So event listener on that select element, when one is chosen we have a function that loads the stuff.
