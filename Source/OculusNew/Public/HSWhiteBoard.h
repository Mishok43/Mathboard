// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HSWhiteBoard.generated.h"

class UTextureRenderTarget2D;
class UStaticMeshComponent;

UCLASS()
class OCULUSNEW_API AHSWhiteBoard : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	AHSWhiteBoard();

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:	
	// Called every frame
	virtual void Tick(float DeltaTime) override;

	UPROPERTY(BlueprintReadWrite)
	bool Version2D;

	UFUNCTION()
	void Update2DFunction();

	UFUNCTION()
	void Update3DFunction();

	UFUNCTION(BlueprintCallable)
	void SaveRenderTargetToDisk(UTextureRenderTarget2D* InRenderTarget, FString Filename) const;
	
	UPROPERTY(EditDefaultsOnly, Category = Materials)
	UMaterialInterface * MasterMaterialRef;

	UPROPERTY(VisibleAnywhere)
	UStaticMeshComponent* FunctionStaticMeshComp;

	UPROPERTY(EditAnywhere)
	class AHSSurfaceViewer* SurfaceViewer;
};
