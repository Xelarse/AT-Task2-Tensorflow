using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MapTileConfigurer : MonoBehaviour
{
    public enum Tile
    {
        CITY_BUILDING,
        ROAD,
        VILLAGE_BUILDING
    }

    //Tile type
    public Tile _tileType;

    //Single
    [SerializeField] private GameObject SINGLE;

    //Singles
    [SerializeField] private GameObject L;
    [SerializeField] private GameObject R;
    [SerializeField] private GameObject T;
    [SerializeField] private GameObject B;

    //Straights
    [SerializeField] private GameObject LR;
    [SerializeField] private GameObject TB;

    //Curves
    [SerializeField] private GameObject TL;
    [SerializeField] private GameObject TR;
    [SerializeField] private GameObject BL;
    [SerializeField] private GameObject BR;

    //3 Ways
    [SerializeField] private GameObject LTR;
    [SerializeField] private GameObject TRB;
    [SerializeField] private GameObject LBR;
    [SerializeField] private GameObject BLT;

    //4way
    [SerializeField] private GameObject TRBL;

    public enum TileConfig
    {
        LR,
        TB,
        TL,
        TR,
        BL,
        BR,
        LTR,
        TRB,
        RBL,
        BLT,
        TRBL,
        SINGLE,
        L,
        R,
        T,
        B
    }

    public void InitTile(TileConfig type)
    {
        switch (type)
        {
            case TileConfig.LR:
                LR.SetActive(true);
                break;
            case TileConfig.TB:
                TB.SetActive(true);
                break;
            case TileConfig.TL:
                TL.SetActive(true);
                break;
            case TileConfig.TR:
                TR.SetActive(true);
                break;
            case TileConfig.BL:
                BL.SetActive(true);
                break;
            case TileConfig.BR:
                BR.SetActive(true);
                break;
            case TileConfig.LTR:
                LTR.SetActive(true);
                break;
            case TileConfig.TRB:
                TRB.SetActive(true);
                break;
            case TileConfig.RBL:
                LBR.SetActive(true);
                break;
            case TileConfig.BLT:
                BLT.SetActive(true);
                break;
            case TileConfig.TRBL:
                TRBL.SetActive(true);
                break;
            case TileConfig.SINGLE:
                SINGLE.SetActive(true);
                break;
            case TileConfig.L:
                L.SetActive(true);
                break;
            case TileConfig.R:
                R.SetActive(true);
                break;
            case TileConfig.T:
                T.SetActive(true);
                break;
            case TileConfig.B:
                B.SetActive(true);
                break;
            default:
                break;
        }
    }
}
