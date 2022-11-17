String.prototype.replaceAt = function(index, replacement) {
  index = parseInt(index)

  // console.log(this)
  // console.log("before: " + this.substring(0, index))
  // console.log("replacement: " + replacement.toString())
  // console.log("after: " + this.substring(index + 1))
  return this.substring(0, index) + replacement.toString() + this.substring(index + 1);
}

var board, game
$(document).ready(function (){
  board = new Board($("#board"))
  game = new Game(board)

  $("[name=depth]").on('input', function(e){
    let val = $("[name=depth]").val()
    if(val < 1)
      $("[name=depth]").val(1)
    else if(val > 9)
      $("[name=depth]").val(9)
    })
});

// var puzzle, solver, player
// $(document).ready(function (){
//   puzzle = new PuzzleUI($(".puzzle"), false)
//   puzzle.reset()
//   puzzle.setState("102345678")

//   solver = new Solver(puzzle)
//   $("#solve").click(function(){
//     try {
//       solver.solve()
      
//     } catch (error) {
//       if(error.name == "DuplicateEntry")
//         Swal.fire({
//           title: "Invalid State",
//           text: error.message,
//           icon: 'error'
//         })
//       else
//         Swal.fire({
//           title: "Unknown Error",
//           icon: 'error'
//         })
//     }
//   })
// });