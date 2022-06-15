------------- Today's total pending locksmiths jobs
SELECT
COUNT(*) AS "Number jobs"
FROM 
(
SELECT
LD.*,
PF.NetCost
FROM [dbo].[Policy_LocksmithDetails] LD
LEFT JOIN [dbo].[Lookup_Locksmiths] LS
ON LD.LocksmithID = LS.ID
LEFT JOIN [dbo].[Policy_Diary] PD
ON LD.ReportID = PD.ReportID
LEFT JOIN [dbo].[Policy_Details] DE
ON PD.ReportID = DE.ReportID
LEFT JOIN [dbo].[Policy_Financial] PF
ON LD.ReportID = PF.ReportID
WHERE LD.Selected = 1
AND LS.LocksmithName LIKE ('WGTK%')
AND PD.Active = 1
AND DE.StatusID <> 15
AND CAST(LD.AvailableFromDate AS DATE) = CAST(GETDATE() AS DATE)
) AS SB
WHERE SB.NetCost IS NULL
ORDER BY COUNT(*) DESC