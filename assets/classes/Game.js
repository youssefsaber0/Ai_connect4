class Game {
  constructor(board) {
    this.board = board
    this.finished = true

    this.game_state = "0000000000000000000"
    this.scores = [0, 0];

    Object.preventExtensions()
  }

  __onListeners() {
    this.board.$("[col]").on('click', function(e){
      let col
      if($(e.target).hasClass("slot"))
        col = $(e.target).closest("[col]").attr('col')
      else
        col = $(e.target).attr('col')
  
      this.apply(col)
    }.bind(this))
  }

  __offListeners() {
    this.board.$("[col]").off('click')
  }

  __botDecision(player_move) {
    $.ajax({
      url: `http://127.0.0.1:5000`,
      data: {
        state: this.game_state,
        col: player_move
      },
      success: function (response) {
        console.log(response)
      }.bind(this),
      error: function(err) {
        Swal.fire({
          title: "Server Failure",
          icon: 'error'
        })
      },
      complete: function() {}
    })
  }

  __showResults() {
    console.log("Showing Results")
  }

  start() {
    this.finished = false;
    this.__onListeners();
  }

  end() {
    this.finished = true
    this.__offListeners();
    this.__showResults()
  }
  
  apply(col) {
    this.board.drop(col, this.turn)
    
    col = this.__botDecision()

    if(parseInt(this.board.state) == 0)
      this.end()
  }
}