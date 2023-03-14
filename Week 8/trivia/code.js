document.addEventListener('DOMContentLoaded', function(){

    // Part 1
    const part1Choices = ['#button1', '#button2', '#button3', '#button4'];
    const part1Answer = '#button4';
    part1Choices.forEach(button => {
        document.querySelector(button).addEventListener('click', function(){
            let currentButton = document.querySelector(button);
            let answerToUser = document.querySelector('#p-part1');
            if (button == part1Answer)
            {
                currentButton.style.background = 'green';
                answerToUser.innerHTML = 'Correct!';
            }
            else
            {
                currentButton.style.background = 'red';
                answerToUser.innerHTML = 'Incorrect!';
            }
        });
    });

    // Part 2
    const part2Answer = 'green'
    document.querySelector('form').addEventListener('submit', function(){
        let response = document.querySelector('#response').value.toLowerCase();
        let answerToUser = document.querySelector('#p-part2');
        if (response == part2Answer)
        {
            document.querySelector('#response').style.background = 'green';
            answerToUser.innerHTML = 'Correct!';
        }
        else
        {
            document.querySelector('#response').style.background = 'red';
            answerToUser.innerHTML = 'Incorrect!';
        }
        event.preventDefault();
    });

})