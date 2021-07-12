import { useEffect, useState } from 'react'
import axios from 'axios'

export default function useProdSearch(query) {

    useEffect(() => {
        axios({
            method: 'GET',
            url: 'http://localhost:5000/products/single',
            params: { id: query }    
        }).then(res => {
            console.log(res.data)
        })
    }, [query])

    return null
}
