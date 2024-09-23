document.addEventListener('DOMContentLoaded',()=>{
    // primero calcula el ancho del browser ventana navegador usando el cliente
    let width = document.body.clientWidth;
    //este calcula toda la info de la pantala del cliente
    let height = window.screen

    console.log(width)

    //Ojo aca el resize O EL EVENTO NO SE CALCULA CON DOCUMENT.TAL SINO WINDOWS
    window.addEventListener("resize",()=>{
        let pic = document.querySelector('#picprofile')
        //pic.style.setProperty('width','200%')
    })
    document.addEventListener('mousemove',(event)=>{
        let x = event.clientX
        let y = event.clientY
        let div = document.querySelector("#mouser")
        div.style.visibility = 'visible'
        //div.style.setProperty('top',`${y}px`)
        //div.style.setProperty('left',`${x}px`)
    })
    
})