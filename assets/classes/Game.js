class Game {
  constructor(board) {
    this.board = board
    this.game_state = "0000000000000000000"

    this.__initListeners()

    Object.preventExtensions()
  }

  __initListeners() {
    this.board.$("[col]").on('click', function (e) {
      if (this.board.turn == this.board.BOT)
        return;

      let col
      if ($(e.target).hasClass("slot"))
        col = $(e.target).closest("[col]").attr('col')
      else
        col = $(e.target).attr('col')

      try {
        this.apply(col)
      }
      catch (e) {
        if (e.name == 'ColumnOverflow')
          Swal.fire({
            title: "Forbidden",
            text: "Column is full",
            icon: "error"
          })
      }
    }.bind(this))
  }

  __botDecision(player_move) {
    $.ajax({
      url: `http://127.0.0.1:5000`,
      data: {
        state: this.game_state,
        col: player_move,
        depth: $("#depth").val(),
        pruning: $("[name=pruning]:checked").val(),
        heureristic: $("[name=heueristic]:checked").val()
      },
      success: function (response) {
        if (this.board.turn == this.board.PLAYER)
          return

        response = JSON.parse(response)
        this.game_state = response.state

        this.board.drop(response.col)

        $("#score1").html(response.scores[0])
        $("#score2").html(response.scores[1])

        if (parseInt(this.board.state) == 0)
          this.end()

      }.bind(this),
      error: function (err) {
        Swal.fire({
          title: "Oops! Server Failure",
          text: "Please Reset",
          icon: 'error'
        })
      },
      complete: function () { }
    })
  }

  end() {
    $(this.board.container).addClass("disabled")

    if (parseInt($("#score1").html()) > parseInt($("#score2").html()))
      Swal.fire({
        title: "Winner",
        color: "green"
      })
    else if(parseInt($("#score1").html()) == parseInt( $("#score2").html()))
      Swal.fire({
        title: "Draw",
        color: "var(--yellow)"
      })

    else {
      Swal.fire({
        title: "Lose",
        color: "var(--red)"
      }) 
    }
  }

  apply(col) {
    this.board.drop(col)

    this.__botDecision(col)
  }

  reset() {
    this.game_state = "0000000000000000000"
    $("#score1").html(0)
    $("#score2").html(0)

    $(this.board.container).removeClass("disabled")
    this.board.$(".yellow-slot").removeClass("yellow-slot")
    this.board.$(".red-slot").removeClass("red-slot")

    this.board.state = "6666666"
    this.board.showTurn(Board.PLAYER)
  }
}